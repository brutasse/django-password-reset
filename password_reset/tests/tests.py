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

    def test_form_custom_search(self):
        # Searching only for email does some extra validation
        form = PasswordRecoveryForm(data={
            'username_or_email': 'barexample.com',
        }, search_fields=['email'])
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username_or_email'],
                         ['Enter a valid e-mail address.'])

        form = PasswordRecoveryForm(data={
            'username_or_email': 'bar@example.com',
        }, search_fields=['email'])
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username_or_email'],
                         ["Sorry, this user doesn't exist."])

        user = User.objects.create_user('test@example.com',
                                        'foo@example.com', 'pass')

        form = PasswordRecoveryForm(data={
            'username_or_email': 'test@example.com',
        }, search_fields=['email'])
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username_or_email'],
                         ["Sorry, this user doesn't exist."])

        # Search by actual email works
        form = PasswordRecoveryForm(data={
            'username_or_email': 'foo@example.com',
        }, search_fields=['email'])
        self.assertTrue(form.is_valid())

        # Now search by username
        user.username = 'username'
        user.save()

        form = PasswordRecoveryForm(data={
            'username_or_email': 'foo@example.com',
        }, search_fields=['username'])
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username_or_email'],
                         ["Sorry, this user doesn't exist."])

        form = PasswordRecoveryForm(data={
            'username_or_email': 'username',
        }, search_fields=['username'])
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
    def setUp(self):
        self.user = User.objects.create_user('foo', 'bar@example.com', 'test')

    def test_recover(self):
        url = reverse('password_reset_recover')
        response = self.client.get(url)
        self.assertContains(response, 'Username or Email')

        response = self.client.post(url, {'username_or_email': 'test'})
        self.assertContains(response, "Sorry, this user")

        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url, {'username_or_email': 'foo'})
        self.assertContains(response, "<strong>bar@example.com</strong>")
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

    def test_email_recover(self):
        url = reverse('email_recover')
        response = self.client.get(url)
        self.assertNotContains(response, "Username or Email")
        self.assertContains(response, "Email:")

        response = self.client.post(url, {'username_or_email': 'foo'})
        self.assertContains(response, "Enter a valid e-mail address")

        response = self.client.post(url, {'username_or_email': 'foo@ex.com'})
        self.assertContains(response, "Sorry, this user")

        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url,
                                    {'username_or_email': 'bar@example.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, '<strong>bar@example.com</strong>')

    def test_username_recover(self):
        url = reverse('username_recover')
        response = self.client.get(url)

        self.assertNotContains(response, "Username or Email")
        self.assertContains(response, "Username:")

        response = self.client.post(url,
                                    {'username_or_email': 'bar@example.com'})
        self.assertContains(response, "Sorry, this user")

        self.assertEqual(len(mail.outbox), 0)
        response = self.client.post(url,
                                    {'username_or_email': 'foo'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertContains(response, '<strong>foo</strong>')
