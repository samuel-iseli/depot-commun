from datetime import datetime, timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from store.models import Customer, Article, ArticleGroup, Purchase
from store.billing import get_billable_purchases, create_invoice, create_invoices


class InvoiceTestBase(TestCase):

    def setUp(self):
        self.customer = self.create_user('Thomas Test')

        self.purchase_datetime = timezone.make_aware(
            datetime(2021, 10, 15, 15, 34)
        )

        self.invoice_datetime = timezone.make_aware(
            datetime(2021, 10, 31, 12, 30)
        )

        self.articles = self.create_test_articles()

    # utility methods
    def create_user(self, name):

        customer = Customer.objects.create(
            name=name,
            street='Teststrasse 121',
            zip='8049',
            city='Zürich'
        )
        customer.save()

        return customer

    def create_test_articles(self):
        # create a group
        self.articlegroup = ArticleGroup.objects.create(
            idx=1,
            name='Item Group'
        )
        self.articlegroup.save()

        # create 2 articles
        article1 = Article.objects.create(
            name='Item 123',
            group=self.articlegroup,
            price=Decimal('1.20')
        )
        article1.save()

        article2 = Article.objects.create(
            name='Item 456',
            group=self.articlegroup,
            price=Decimal('4.50')
        )
        article2.save()

        return [article1, article2]

    def create_purchases(self, customer, datetime, articles):
        purchases = []
        for article in articles:
            i_p = Purchase.objects.create(
                customer=customer,
                article=article,
                date=datetime,
                quantity=1,
                price=article.price
            )
            i_p.save()
            purchases.append(i_p)

        return purchases


class InvoiceTest(InvoiceTestBase):

    def test_get_billable_purchases(self):
        self.create_purchases(
            self.customer, self.purchase_datetime,
            self.articles
        )

        no_purchases = get_billable_purchases(
            self.purchase_datetime + timedelta(days=-1)
        )

        self.assertEquals(0, len(no_purchases))

        some_purchases = get_billable_purchases(
            self.purchase_datetime + timedelta(days=1)
        )

        # we should get a dictionary with 1 purchase for 1 customer
        self.assertEquals(1, len(some_purchases.keys()))
        self.assertEquals(1, len(some_purchases.values()))

    def test_create_invoice(self):
        # create 2 purchases
        p1 = Purchase(
            customer=self.customer,
            article=self.articles[0],
            quantity=2,
            price=self.articles[0].price
        )
        p1.save()
        p2 = Purchase(
            customer=self.customer,
            article=self.articles[1],
            quantity=1,
            price=self.articles[1].price
        )
        p2.save()

        invoice = create_invoice(
            self.customer, self.invoice_datetime,
            [p1, p2]
            )

        self.assertEquals(self.customer, invoice.customer)
        self.assertEquals(2, len(invoice.purchases.all()))
        expected_amount = Decimal(
            f'{2 * self.articles[0].price + self.articles[1].price:.2f}')
        self.assertEquals(expected_amount, invoice.amount)

    def test_modify_invoice(self):
        """
        add an additional item to an invoice.
        this should change the invoice amount.
        """
        # create 2 item purchases
        p1 = Purchase(
            customer=self.customer,
            article=self.articles[0],
            quantity=2,
            price=self.articles[0].price
        )
        p1.save()
        p2 = Purchase(
            customer=self.customer,
            article=self.articles[1],
            quantity=2,
            price=self.articles[1].price
        )
        p2.save()

        # create invoice with p1
        invoice = create_invoice(
            self.customer, self.invoice_datetime,
            [p1]
            )

        self.assertEquals(
            Decimal(f'{2 * self.articles[0].price}'),
            invoice.amount)

        # add purchase p2
        p2.invoice = invoice
        p2.save()
        invoice.save()

        self.assertEquals(
            Decimal(f'{2 * self.articles[0].price + 2 * self.articles[1].price:.2f}'),
            invoice.amount
        )

    def test_validate_purchase(self):
        """
        add purchase to an invoice
        make sure that customer and price are set automatically
        by validation logic (clean())
        """
        # create empty invoice
        invoice = create_invoice(
            self.customer, self.invoice_datetime,
            []
            )

        # add purchase without specifying price or customer
        p1 = Purchase(
            invoice=invoice,
            article=self.articles[0],
            quantity=2,
        )
        p1.clean()
        
        self.assertEquals(self.customer, p1.customer)
        self.assertEquals(self.articles[0].price, p1.price)

        p1.save()

        self.assertEquals(
            Decimal(f'{2 * p1.price:0.2f}'),
            invoice.amount
        )

    def test_delete_purchase(self):
        """
        for admin operations we need to invoice to be updated
        when a purchase is deleted.
        """
        p1 = Purchase(
            customer=self.customer,
            article=self.articles[0],
            quantity=2,
            price=self.articles[0].price
        )
        p1.save()
        p2 = Purchase(
            customer=self.customer,
            article=self.articles[1],
            quantity=2,
            price=self.articles[1].price
        )
        p2.save()

        # create invoice with p1 and ps
        invoice = create_invoice(
            self.customer, self.invoice_datetime,
            [p1, p2]
            )
        self.assertEquals(
            Decimal(f'{2 * self.articles[0].price + 2 * self.articles[1].price:.2f}'),
            invoice.amount
        )

        # delete p1
        p1.delete()

        self.assertEquals(
            Decimal(f'{2 * self.articles[1].price:.2f}'),
            invoice.amount
        )


class InvoiceTestsMultiUsers(InvoiceTestBase):
    def setUp(self):
        super().setUp()

        self.user2 = self.create_user('Hans Muster')

        self.purchases1 = self.create_purchases(
            self.customer, self.purchase_datetime,
            self.articles
        )

        self.purchases2 = self.create_purchases(
            self.customer, self.purchase_datetime,
            self.articles[0:1]
        )

        self.purchases3 = self.create_purchases(
            self.user2, self.purchase_datetime,
            self.articles
        )

    def test_get_billable_purchases_multiple_user(self):

        billables = get_billable_purchases(self.purchase_datetime)

        # we should get dictionary for 2 users
        self.assertEquals(2, len(billables))

        # self.customer has 3 purchases, user2 has 2
        self.assertEquals(3, len(billables[self.customer]))
        self.assertEquals(2, len(billables[self.user2]))

    def test_create_invoice(self):
        invoice = create_invoice(
            self.customer, self.invoice_datetime,
            self.purchases1 + self.purchases2)

        self.assertEquals(Decimal('6.9'), invoice.amount)
        self.assertEquals(self.invoice_datetime, invoice.date)
        # purchase1 has 2 items, purchase2 1
        self.assertEquals(3, len(invoice.purchases.all()))

    def test_create_invoices(self):
        invoices = create_invoices(
            self.invoice_datetime, self.invoice_datetime)

        self.assertEquals(2, len(invoices))

        self.assertEquals(self.customer, invoices[0].customer)
        self.assertEquals(Decimal('6.9'), invoices[0].amount)

        self.assertEquals(self.user2, invoices[1].customer)
        self.assertEquals(Decimal('5.7'), invoices[1].amount)
