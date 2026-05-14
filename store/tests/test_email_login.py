import re

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from store.models import Customer


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class EmailLoginTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='mail-user',
            email='mail-user@example.com',
            password='unused-password',
        )
        Customer.objects.create(
            user=self.user,
            name='Mail User Customer',
            street='Main Street 1',
            zip='8000',
            city='Zurich',
        )

    def test_anonymous_home_redirects_to_custom_login(self):
        response = self.client.get(reverse('store:home'))
        self.assertRedirects(response, f"{reverse('store:email-login')}?next=/store/")

    def test_custom_login_page_contains_unobtrusive_admin_link(self):
        response = self.client.get(reverse('store:email-login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('admin:login'))
        self.assertContains(response, 'Benutzername/Passwort')

    def test_post_email_sends_confirmation_link(self):
        response = self.client.post(
            reverse('store:email-login'),
            {'email': 'mail-user@example.com', 'next': '/store/'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anmelde-Link gesendet')

        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/store/login/confirm/', mail.outbox[0].body)

    def test_confirmation_link_logs_in_user(self):
        self.client.post(
            reverse('store:email-login'),
            {'email': 'mail-user@example.com', 'next': '/store/'},
        )

        from django.core import mail
        body = mail.outbox[0].body
        match = re.search(r'http://testserver(/store/login/confirm/\S+)', body)
        self.assertIsNotNone(match)

        response = self.client.get(match.group(1))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/store/')

        response_after_login = self.client.get(reverse('store:home'))
        self.assertEqual(response_after_login.status_code, 200)

    def test_invalid_confirmation_link_shows_error(self):
        response = self.client.get('/store/login/confirm/invalid/invalid/')
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Link ist ungültig oder abgelaufen', status_code=400)
