import datetime

from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth.hashers import get_hasher

from django.views.decorators.debug import sensitive_post_parameters
from .compat import get_current_site, get_user_model, get_username
from .forms import PasswordRecoveryForm, PasswordResetForm
from .signals import user_recovers_password


class SaltMixin(object):
    salt = 'password_recovery'
    url_salt = 'password_recovery_url'

    def hash_password(self, psw):
        return get_hasher().encode(psw, self.salt)


def loads_with_timestamp(value, salt):
    """Returns the unsigned value along with its timestamp, the time when it
    got dumped."""
    try:
        signing.loads(value, salt=salt, max_age=-999999)
    except signing.SignatureExpired as e:
        age = float(str(e).split('Signature age ')[1].split(' >')[0])
        timestamp = timezone.now() - datetime.timedelta(seconds=age)
        return timestamp, signing.loads(value, salt=salt)


class RecoverDone(SaltMixin, generic.TemplateView):
    template_name = "password_reset/reset_sent.html"

    def get_context_data(self, **kwargs):
        ctx = super(RecoverDone, self).get_context_data(**kwargs)
        try:
            ctx['timestamp'], ctx['email'] = loads_with_timestamp(
                self.kwargs['signature'], salt=self.url_salt,
            )
        except signing.BadSignature:
            raise Http404
        return ctx


recover_done = RecoverDone.as_view()


class RecoverFailed(SaltMixin, generic.TemplateView):
    template_name = 'password_reset/reset_sent_failed.html'

    def get_context_data(self, **kwargs):
        ctx = super(RecoverFailed, self).get_context_data(**kwargs)
        try:
            ctx['timestamp'], ctx['email'] = loads_with_timestamp(
                self.kwargs['signature'], salt=self.url_salt,
            )
        except signing.BadSignature:
            raise Http404
        return ctx
recover_failed = RecoverFailed.as_view()


class Recover(SaltMixin, generic.FormView):
    case_sensitive = True
    form_class = PasswordRecoveryForm
    template_name = 'password_reset/recovery_form.html'
    success_url_name = 'password_reset_sent'
    failure_url_name = 'password_reset_sent_failed'
    email_template_name = 'password_reset/recovery_email.txt'
    email_html_template_name = 'password_reset/recovery_email.html'
    email_subject_template_name = 'password_reset/recovery_email_subject.txt'
    search_fields = ['username', 'email']
    sent_success = 0

    def get_success_url(self):
        if self.sent_success:
            return reverse(self.success_url_name, args=[self.mail_signature])
        else:
            return reverse(self.failure_url_name, args=[self.mail_signature])

    def get_context_data(self, **kwargs):
        kwargs['url'] = self.request.get_full_path()
        return super(Recover, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(Recover, self).get_form_kwargs()

        if hasattr(settings, 'PASSWORD_RESET_CASE_SENSITIVE'):
            self.case_sensitive = settings.PASSWORD_RESET_CASE_SENSITIVE

        kwargs.update({
            'case_sensitive': self.case_sensitive,
            'search_fields': self.search_fields,
        })
        return kwargs

    def get_site(self):
        return get_current_site(self.request)

    def send_notification(self):
        context = {
            'site': self.get_site(),
            'user': self.user,
            'username': get_username(self.user),
            'token': signing.dumps(
                {
                    'pk': self.user.pk,
                    'psw': self.hash_password(
                        self.user.password
                    )
                },
                salt=self.salt),
            'secure': self.request.is_secure(),
        }
        text_content = loader.render_to_string(
            self.email_template_name, context).strip()
        html_content = loader.render_to_string(
            self.email_html_template_name, context).strip()
        subject = loader.render_to_string(
            self.email_subject_template_name, context).strip()

        msg = EmailMultiAlternatives(
            subject, text_content,
            settings.DEFAULT_FROM_EMAIL, [self.user.email, ])
        msg.attach_alternative(html_content, 'text/html')
        result = msg.send(fail_silently=True)
        return result

    def form_valid(self, form):
        self.user = form.cleaned_data['user']
        self.sent_success = self.send_notification()
        if (
                len(self.search_fields) == 1 and
                self.search_fields[0] == 'username'
        ):
            # if we only search by username, don't disclose the user email
            # since it may now be public information.
            email = self.user.username
        else:
            email = self.user.email
        self.mail_signature = signing.dumps(email, salt=self.url_salt)
        return super(Recover, self).form_valid(form)


recover = Recover.as_view()


class Reset(SaltMixin, generic.FormView):
    form_class = PasswordResetForm
    token_expires = 3600 * 48  # Two days
    template_name = 'password_reset/reset.html'
    success_url = reverse_lazy('password_reset_done')

    def get_token_expires(self):
        duration = getattr(settings, 'PASSWORD_RESET_TOKEN_EXPIRES',
                           self.token_expires)
        if duration is None:
            duration = 3600 * 48  # Two days
        return duration

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = None

        try:
            unsigned_pk_hash = signing.loads(kwargs['token'],
                                             max_age=self.token_expires,
                                             salt=self.salt)
        except signing.BadSignature:
            return self.invalid()

        try:
            pk = unsigned_pk_hash['pk']
            password = unsigned_pk_hash['psw']
        except KeyError:
            return self.invalid()

        self.user = get_object_or_404(get_user_model(), pk=pk)

        # Ensure the hashed password is same to prevent link to be reused
        # TODO: this is assuming the password is changed
        if password != self.hash_password(self.user.password):
            return self.invalid()

        return super(Reset, self).dispatch(request, *args, **kwargs)

    def invalid(self):
        return self.render_to_response(self.get_context_data(invalid=True))

    def get_form_kwargs(self):
        kwargs = super(Reset, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(Reset, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'username': get_username(self.user),
                'token': self.kwargs['token'],
            })
        return ctx

    def form_valid(self, form):
        form.save()
        user_recovers_password.send(
            sender=get_user_model(),
            user=form.user,
            request=self.request
        )
        return redirect(self.get_success_url())


reset = Reset.as_view()


class ResetDone(generic.TemplateView):
    template_name = 'password_reset/recovery_done.html'


reset_done = ResetDone.as_view()
