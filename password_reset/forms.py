from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import validate_email
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .compat import get_user_model

error_messages = {
    'not_found': _("Sorry, this user doesn't exist."),
    'password_mismatch': _("The two passwords didn't match."),
}

try:
    # must be installed before.
    if 'captcha' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured("captcha is not installed.")

    # uses django-simple-captcha
    from captcha.fields import CaptchaField


    class CaptchaForm(forms.Form):
        captcha = CaptchaField(label=_('Captcha'))  # Optional Captcha

        def order_fields(self, field_order):
            """https://docs.djangoproject.com/en/1.9/ref/forms/api/#django.forms.Form.order_fields"""
            # Put the captcha at the bottom of the form
            field_name = "captcha"
            if field_order is None:
                field_order = self.fields.keys()
            field_order.pop(field_order.index(field_name))
            field_order.append(field_name)
            return super(CaptchaForm, self).order_fields(field_order)


except (ImproperlyConfigured, ImportError):
    CaptchaForm = forms.Form


class PasswordRecoveryForm(CaptchaForm):
    username_or_email = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.case_sensitive = kwargs.pop('case_sensitive', True)
        search_fields = kwargs.pop('search_fields', ('username', 'email'))
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)

        message = ("No other fields than username and email are supported "
                   "by default")
        if len(search_fields) not in (1, 2):
            raise ValueError(message)
        for field in search_fields:
            if field not in ['username', 'email']:
                raise ValueError(message)

        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'both': _('Username or Email'),
        }
        User = get_user_model()  # noqa
        if getattr(User, 'USERNAME_FIELD', 'username') == 'email':
            self.label_key = 'email'
        elif len(search_fields) == 1:
            self.label_key = search_fields[0]
        else:
            self.label_key = 'both'
        self.fields['username_or_email'].label = labels[self.label_key]

    def clean_username_or_email(self):
        username = self.cleaned_data['username_or_email']
        cleaner = getattr(self, 'get_user_by_%s' % self.label_key)
        self.cleaned_data['user'] = user = cleaner(username)

        user_is_active = getattr(user, 'is_active', True)
        recovery_only_active_users = getattr(settings,
                                             'RECOVER_ONLY_ACTIVE_USERS',
                                             False)

        if recovery_only_active_users and not user_is_active:
            raise forms.ValidationError(_("Sorry, inactive users can't "
                                          "recover their password."))

        return username

    def get_user(self, *args, **kwargs):
        """ Method used to customize how to get the user into subclasses.
        :rtype: User object
        """
        return get_user_model()._default_manager.get(*args, **kwargs)

    def get_user_by_username(self, username):
        key = 'username__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = self.get_user(**{key: username})
        except User.DoesNotExist:
            raise forms.ValidationError(error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_email(self, email):
        validate_email(email)
        key = 'email__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = self.get_user(**{key: email})
        except User.DoesNotExist:
            raise forms.ValidationError(error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_both(self, username):
        key = '__%sexact'
        key = key % '' if self.case_sensitive else key % 'i'

        def f(field):  # to satisfy lint in Travis auto build on Github
            return Q(**{field + key: username})

        filters = f('username') | f('email')
        User = get_user_model()
        try:
            user = self.get_user(filters)
        except User.DoesNotExist:
            raise forms.ValidationError(error_messages['not_found'],
                                        code='not_found')
        except User.MultipleObjectsReturned:
            raise forms.ValidationError(_("Unable to find user."))

        return user


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('New password (confirm)'),
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(
                error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            get_user_model()._default_manager.filter(pk=self.user.pk).update(
                password=self.user.password,
            )
        return self.user
