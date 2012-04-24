from django.contrib.auth.models import User
from django.test import TestCase

from ..forms import PasswordRecoveryForm, PasswordResetForm


class FormTests(TestCase):
    def test_username_input(self):
        form = PasswordRecoveryForm()
        self.assertFalse(form.is_valid())

        form = PasswordRecoveryForm(data={'username_or_email': 'inexisting'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username_or_email'],
                         ["Sorry, this user doesn't exist."])

        user = User.objects.create_user('foo', 'bar@example.com', 'pass')

        form = PasswordRecoveryForm(data={
            'username_or_email': 'foo',
        })
        self.assertTrue(form.is_valid())

        form = PasswordRecoveryForm(data={
            'username_or_email': 'FOO',
        })
        self.assertFalse(form.is_valid())

        form = PasswordRecoveryForm(data={
            'username_or_email': 'FOO',
        }, case_sensitive=False)
        self.assertTrue(form.is_valid())

        form = PasswordRecoveryForm(data={
            'username_or_email': 'bar@example.com',
        })
        self.assertTrue(form.is_valid())

        form = PasswordRecoveryForm(data={
            'username_or_email': 'bar@example.COM',
        })
        self.assertFalse(form.is_valid())

        form = PasswordRecoveryForm(data={
            'username_or_email': 'bar@example.COM',
        }, case_sensitive=False)
        self.assertTrue(form.is_valid())

    def test_password_reset_form(self):
        user = User.objects.create_user('foo', 'bar@example.com', 'pass')
        old_sha = user.password

        form = PasswordResetForm(user=user)
        self.assertFalse(form.is_valid())

        form = PasswordResetForm(user=user, data={'password1': 'foo'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'],
                         ['This field is required.'])

        form = PasswordResetForm(user=user, data={'password1': 'foo',
                                                  'password2': 'bar'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'],
                         ["The two passwords didn't match."])

        form = PasswordResetForm(user=user, data={'password1': 'foo',
                                                  'password2': 'foo'})
        self.assertTrue(form.is_valid())
        self.assertEqual(user.password, old_sha)
        form.save()
        self.assertNotEqual(user.password, old_sha)
