from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _


class PasswordRecoveryForm(forms.Form):
    username_or_email = forms.CharField(
        label=_('Username or Email'),
    )

    def __init__(self, *args, **kwargs):
        self.case_sensitive = kwargs.pop('case_sensitive', True)
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)

    def clean_username_or_email(self):
        username = self.cleaned_data['username_or_email']
        try:
            validate_email(username)
            key = 'email'
        except forms.ValidationError:
            key = 'username'
        key = '%s__exact' % key if self.case_sensitive else '%s__iexact' % key
        try:
            self.cleaned_data['user'] = User.objects.get(**{key: username})
        except User.DoesNotExist:
            raise forms.ValidationError(_("Sorry, this user doesn't exist."))
        return username


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
            raise forms.ValidationError(_("The two passwords didn't match."))
        return password2

    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        User.objects.filter(pk=self.user.pk).update(
            password=self.user.password,
        )
