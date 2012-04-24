from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from .. import views
from ..forms import PasswordRecoveryForm, PasswordResetForm


class FormTests(TestCase):
    def test_username_input(self):
        form = PasswordRecoveryForm()
        self.assertFalse(form.is_valid())

        form = PasswordRecoveryForm(data={'username_or_email': 'inexisting'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username_or_email'],
                         ["Sorry, this user doesn't exist."])

        User.objects.create_user('foo', 'bar@example.com', 'pass')

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


class ViewTests(TestCase):
    urls = 'password_reset.urls'

    def setUp(self):
        self.user = User.objects.create_user('foo', 'bar@example.com', 'test')
        self.factory = RequestFactory()

    def test_recover(self):
        url = reverse('password_reset_recover')
        request = self.factory.get(url)
        response = views.recover(request)
        self.assertContains(response, 'Username or Email')

        request = self.factory.post(url, {'username_or_email': 'test'})
        response = views.recover(request)
        self.assertContains(response, "Sorry, this user")

        request = self.factory.post(url, {'username_or_email': 'foo'})
        self.assertEqual(len(mail.outbox), 0)
        response = views.recover(request)
        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]

        self.assertEqual(message.subject,
                         u'Password recovery on testserver')

        self.assertTrue('Dear foo,' in message.body)

        url = message.body.split('http://testserver')[1].split('\n', 1)[0]

        response = self.client.get(url)
        self.assertContains(response, 'New password (confirm)')
        self.assertContains(response, 'Hi, <strong>foo</strong>')

        data = {'password1': 'foo',
                'password2': 'foo'}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertContains(response,
                            "Your password has successfully been reset.")

    def test_invalid_reset_link(self):
        url = reverse('password_reset_reset', args=['foobar-invalid'])

        response = self.client.get(url)
        self.assertContains(response,
                            "Sorry, this password reset link is invalid")
