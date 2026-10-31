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
        customer = Customer.objects.create(
            name='Mail User Customer',
            street='Main Street 1',
            zip='8000',
            city='Zurich',
        )
        customer.users.add(self.user)

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

    def test_confirmation_link_shows_confirmation_then_logs_in_user(self):
        self.client.post(
            reverse('store:email-login'),
            {'email': 'mail-user@example.com', 'next': '/store/'},
        )

        from django.core import mail
        body = mail.outbox[0].body
        match = re.search(r'http://testserver(/store/login/confirm/\S+)', body)
        self.assertIsNotNone(match)

        response = self.client.get(match.group(1))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login bestätigen')

        response_post = self.client.post(match.group(1), {'next': '/store/'})
        self.assertEqual(response_post.status_code, 200)
        self.assertContains(response_post, 'Login bestätigt')

        # confirming does not log in the confirming browser; the polling device does
        self.assertEqual(self.client.get(reverse('store:home')).status_code, 302)
        self.assertEqual(self.client.get(reverse('store:email-login-status')).json()['status'], 'ok')
        self.assertEqual(self.client.get(reverse('store:home')).status_code, 200)

    def test_invalid_confirmation_link_shows_error(self):
        response = self.client.get('/store/login/confirm/invalid/invalid/')
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Link ist ungültig oder abgelaufen', status_code=400)

    def test_post_email_creates_user_for_matching_customers_and_sends_confirmation(self):
        Customer.objects.create(
            name='Fresh Customer One',
            email='new-login@example.com',
            street='Street 1',
            zip='8000',
            city='Zurich',
        )
        Customer.objects.create(
            name='Fresh Customer Two',
            email='new-login@example.com',
            street='Street 2',
            zip='8000',
            city='Zurich',
        )

        response = self.client.post(
            reverse('store:email-login'),
            {'email': 'new-login@example.com', 'next': '/store/'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Anmelde-Link gesendet')

        user_model = get_user_model()
        created_user = user_model.objects.filter(email='new-login@example.com').first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.customers.count(), 2)

        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/store/login/confirm/', mail.outbox[0].body)

    def test_post_email_does_not_reassign_customer_with_existing_user(self):
        user_model = get_user_model()
        existing_user = user_model.objects.create_user(
            username='already-linked',
            email='already-linked@example.com',
            password='unused-password',
        )
        kept_customer = Customer.objects.create(
            name='Already Linked',
            email='shared-login@example.com',
            street='Street 1',
            zip='8000',
            city='Zurich',
        )
        kept_customer.users.add(existing_user)
        adopted_customer = Customer.objects.create(
            name='Adopted Customer',
            email='shared-login@example.com',
            street='Street 2',
            zip='8000',
            city='Zurich',
        )

        response = self.client.post(
            reverse('store:email-login'),
            {'email': 'shared-login@example.com', 'next': '/store/'},
        )

        self.assertEqual(response.status_code, 200)

        kept_customer.refresh_from_db()
        adopted_customer.refresh_from_db()

        self.assertTrue(kept_customer.users.filter(id=existing_user.id).exists())
        self.assertEqual(kept_customer.users.count(), 1)
        self.assertEqual(adopted_customer.users.count(), 1)
        self.assertNotEqual(adopted_customer.users.first().id, existing_user.id)

        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)

    def _request_login(self, client):
        client.post(
            reverse('store:email-login'),
            {'email': 'mail-user@example.com', 'next': '/store/'},
        )
        from django.core import mail
        match = re.search(r'http://testserver(/store/login/confirm/\S+)', mail.outbox[-1].body)
        return match.group(1)

    def test_polling_device_is_logged_in_after_link_confirmed_elsewhere(self):
        from django.test import Client
        pwa = Client()
        link = self._request_login(pwa)
        self.assertIn('lr=', link)

        status_url = reverse('store:email-login-status')
        self.assertEqual(pwa.get(status_url).json()['status'], 'pending')

        safari = Client()
        safari.post(link, {'next': '/store/'})

        self.assertEqual(pwa.get(status_url).json(), {'status': 'ok', 'next': '/store/'})
        self.assertEqual(pwa.get(reverse('store:home')).status_code, 200)

    def test_other_device_cannot_poll_without_session(self):
        from django.test import Client
        pwa = Client()
        link = self._request_login(pwa)
        Client().post(link, {'next': '/store/'})

        attacker = Client()
        self.assertEqual(attacker.get(reverse('store:email-login-status')).json()['status'], 'expired')

    def test_login_request_is_single_use(self):
        from django.test import Client
        from store.models import LoginRequest
        pwa = Client()
        link = self._request_login(pwa)
        Client().post(link, {'next': '/store/'})
        pwa.get(reverse('store:email-login-status'))
        self.assertTrue(LoginRequest.objects.get().consumed)

    def test_expired_login_request_is_not_approved(self):
        from datetime import timedelta
        from django.test import Client
        from django.utils import timezone
        from store.models import LoginRequest
        pwa = Client()
        link = self._request_login(pwa)
        LoginRequest.objects.update(created=timezone.now() - timedelta(hours=1))
        Client().post(link, {'next': '/store/'})
        self.assertEqual(pwa.get(reverse('store:email-login-status')).json()['status'], 'expired')
