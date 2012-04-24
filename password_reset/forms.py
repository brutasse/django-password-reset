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
            user = User.objects.get(**{key: username})
        except User.DoesNotExist:
            raise forms.ValidationError(_("Sorry, this user doesn't exist."))
        return username
