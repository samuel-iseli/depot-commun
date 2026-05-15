from decimal import Decimal

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from store.admin import InvoiceBasketInline, InvoicePurchaseForm
from store.models import Article, ArticleGroup, Customer, Invoice, Purchase, ShoppingBasket


class InvoicePurchaseInlineTest(TestCase):
    def setUp(self):
        self.group = ArticleGroup.objects.create(idx=1, name='Group')
        self.active_article = Article.objects.create(
            group=self.group,
            sortidx=1,
            name='Active article',
            price=Decimal('1.20'),
            active=True,
        )
        self.inactive_article = Article.objects.create(
            group=self.group,
            sortidx=2,
            name='Inactive article',
            price=Decimal('2.50'),
            active=False,
        )
        self.customer = Customer.objects.create(
            name='Test Customer',
            street='Example Street 1',
            zip='8000',
            city='Zurich',
        )
        self.invoice = Invoice.objects.create(customer=self.customer)

    def _widget_choice_ids(self, form):
        ids = []
        for choice_value, _ in form.fields['article'].widget.choices:
            if choice_value in ('', None):
                continue
            ids.append(int(str(choice_value)))
        return ids

    def test_new_form_filters_out_inactive_articles_in_widget(self):
        form = InvoicePurchaseForm()

        self.assertListEqual(
            self._widget_choice_ids(form),
            [self.active_article.pk],
        )

    def test_existing_purchase_with_inactive_article_is_valid(self):
        purchase = Purchase.objects.create(
            article=self.inactive_article,
            quantity=2,
            price=self.inactive_article.price,
            customer=self.customer,
            invoice=self.invoice,
            date=timezone.now(),
        )

        form = InvoicePurchaseForm(
            instance=purchase,
            data={
                'article': str(self.inactive_article.pk),
                'quantity': '2',
                'price': str(self.inactive_article.price),
                'customer': str(self.customer.pk),
                'invoice': str(self.invoice.pk),
                'date': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            },
        )

        self.assertTrue(form.is_valid(), form.errors.as_json())
        self.assertQuerySetEqual(
            form.fields['article'].queryset.order_by('pk'),
            [self.active_article, self.inactive_article],
            transform=lambda article: article,
        )

        self.assertListEqual(
            self._widget_choice_ids(form),
            [self.active_article.pk, self.inactive_article.pk],
        )


class InvoiceBasketInlineTest(TestCase):
    def setUp(self):
        self.group = ArticleGroup.objects.create(idx=1, name='Group')
        self.article = Article.objects.create(
            group=self.group,
            sortidx=1,
            name='Article',
            price=Decimal('2.50'),
            active=True,
        )
        self.customer = Customer.objects.create(
            name='Test Customer',
            street='Example Street 1',
            zip='8000',
            city='Zurich',
        )
        self.invoice = Invoice.objects.create(customer=self.customer)
        self.basket = ShoppingBasket.objects.create(
            customer=self.customer,
            invoice=self.invoice,
            completed=timezone.now(),
        )
        Purchase.objects.create(
            article=self.article,
            quantity=2,
            price=Decimal('2.50'),
            customer=self.customer,
            invoice=self.invoice,
            basket=self.basket,
            date=timezone.now(),
        )
        Purchase.objects.create(
            article=self.article,
            quantity=1,
            price=Decimal('3.00'),
            customer=self.customer,
            invoice=self.invoice,
            basket=self.basket,
            date=timezone.now(),
        )
        self.inline = InvoiceBasketInline(Invoice, AdminSite())

    def test_purchase_count_and_total(self):
        self.assertEqual(self.inline.purchase_count(self.basket), 2)
        self.assertEqual(self.inline.purchase_total(self.basket), Decimal('8.00'))


class InvoiceAdminBasketGenerationTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(self.admin_user)

        self.group = ArticleGroup.objects.create(idx=1, name='Group')
        self.article = Article.objects.create(
            group=self.group,
            sortidx=1,
            name='Article',
            price=Decimal('2.50'),
            active=True,
        )

        self.customer = Customer.objects.create(
            name='Test Customer',
            street='Example Street 1',
            zip='8000',
            city='Zurich',
        )
        self.other_customer = Customer.objects.create(
            name='Other Customer',
            street='Example Street 2',
            zip='8001',
            city='Zurich',
        )

    def test_generate_basket_invoices_creates_invoices_for_completed_uninvoiced_baskets(self):
        completed_basket = ShoppingBasket.objects.create(
            customer=self.customer,
            completed=timezone.now(),
        )
        Purchase.objects.create(
            article=self.article,
            quantity=2,
            price=Decimal('2.50'),
            customer=self.customer,
            basket=completed_basket,
        )

        second_completed_basket = ShoppingBasket.objects.create(
            customer=self.customer,
            completed=timezone.now(),
        )
        Purchase.objects.create(
            article=self.article,
            quantity=1,
            price=Decimal('3.00'),
            customer=self.customer,
            basket=second_completed_basket,
        )

        ignored_open_basket = ShoppingBasket.objects.create(customer=self.customer)
        Purchase.objects.create(
            article=self.article,
            quantity=4,
            price=Decimal('1.00'),
            customer=self.customer,
            basket=ignored_open_basket,
        )

        existing_invoice = Invoice.objects.create(customer=self.other_customer, amount=Decimal('0.00'))
        already_invoiced_basket = ShoppingBasket.objects.create(
            customer=self.other_customer,
            completed=timezone.now(),
            invoice=existing_invoice,
        )
        Purchase.objects.create(
            article=self.article,
            quantity=1,
            price=Decimal('5.00'),
            customer=self.other_customer,
            basket=already_invoiced_basket,
            invoice=existing_invoice,
        )

        response = self.client.get(reverse('admin:store_invoice_create_basket_invoices'))

        self.assertRedirects(response, reverse('admin:store_invoice_changelist'))
        self.assertEqual(Invoice.objects.count(), 2)

        generated_invoice = Invoice.objects.exclude(pk=existing_invoice.pk).get()
        self.assertEqual(generated_invoice.customer, self.customer)
        self.assertEqual(generated_invoice.amount, Decimal('8.00'))
        self.assertQuerySetEqual(
            generated_invoice.baskets.order_by('pk'),
            [completed_basket, second_completed_basket],
            transform=lambda basket: basket,
        )

        completed_basket.refresh_from_db()
        second_completed_basket.refresh_from_db()
        ignored_open_basket.refresh_from_db()
        already_invoiced_basket.refresh_from_db()

        self.assertEqual(completed_basket.invoice_id, generated_invoice.id)
        self.assertEqual(second_completed_basket.invoice_id, generated_invoice.id)
        self.assertIsNone(ignored_open_basket.invoice_id)
        self.assertEqual(already_invoiced_basket.invoice_id, existing_invoice.id)