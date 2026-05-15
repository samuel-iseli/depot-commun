from decimal import Decimal

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
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