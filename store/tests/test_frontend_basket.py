from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from store.models import Article, ArticleGroup, Customer, Purchase, ShoppingBasket


class BasketFrontendViewTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='Frontend User',
            street='Main Street 1',
            zip='8000',
            city='Zurich',
        )
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='frontend-user',
            password='test-pass-123',
            customer=self.customer,
        )
        self.client.force_login(self.user)

        self.group = ArticleGroup.objects.create(idx=1, name='Food')
        self.article = Article.objects.create(
            group=self.group,
            sortidx=1,
            name='Bread',
            price=Decimal('3.20'),
            active=True,
        )

    def test_new_basket_redirects_to_existing_open_basket(self):
        open_basket = ShoppingBasket.objects.create(customer=self.customer)

        response = self.client.post(reverse('store:new-basket'))

        self.assertRedirects(response, f"/store/basket/{open_basket.id}/")
        self.assertEqual(
            ShoppingBasket.objects.filter(customer=self.customer, completed__isnull=True).count(),
            1,
        )

    def test_finish_basket_confirmation_and_cancel_then_confirm(self):
        basket = ShoppingBasket.objects.create(customer=self.customer)
        Purchase.objects.create(
            article=self.article,
            quantity=2,
            price=self.article.price,
            customer=self.customer,
            basket=basket,
        )

        confirm_response = self.client.get(reverse('store:finish-basket', args=[basket.id]))
        self.assertEqual(confirm_response.status_code, 200)
        self.assertContains(confirm_response, 'Einkauf abschliessen?')
        self.assertContains(confirm_response, 'Bread')

        cancel_response = self.client.post(
            reverse('store:finish-basket', args=[basket.id]),
            {'action': 'cancel'},
        )
        self.assertRedirects(cancel_response, f'/store/basket/{basket.id}/')
        basket.refresh_from_db()
        self.assertIsNone(basket.completed)

        confirm_post_response = self.client.post(
            reverse('store:finish-basket', args=[basket.id]),
            {'action': 'confirm'},
        )
        self.assertRedirects(confirm_post_response, '/store/')
        basket.refresh_from_db()
        self.assertIsNotNone(basket.completed)

    def test_finish_basket_delete_removes_incomplete_basket(self):
        basket = ShoppingBasket.objects.create(customer=self.customer)
        purchase = Purchase.objects.create(
            article=self.article,
            quantity=1,
            price=self.article.price,
            customer=self.customer,
            basket=basket,
        )

        response = self.client.post(
            reverse('store:finish-basket', args=[basket.id]),
            {'action': 'delete'},
        )

        self.assertRedirects(response, '/store/')
        self.assertFalse(ShoppingBasket.objects.filter(id=basket.id).exists())
        self.assertFalse(Purchase.objects.filter(id=purchase.id).exists())

    def test_home_lists_open_baskets_and_disables_new_basket_action(self):
        basket = ShoppingBasket.objects.create(customer=self.customer)

        response = self.client.get(reverse('store:home'))

        self.assertContains(response, 'Offene Einkaeufe')
        self.assertContains(response, f'/store/basket/{basket.id}/')
        self.assertContains(response, 'disabled="true"')
