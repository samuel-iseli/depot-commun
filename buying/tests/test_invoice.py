from datetime import datetime, timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone

from buying.models import Depot, UserProfile, Item, ItemGroup, Purchase, ItemPurchase
from buying.billing import get_billable_purchases, create_invoice_from_purchases, create_invoice, create_invoices


class InvoiceTestBase(TestCase):

    def setUp(self):
        self.depot = Depot.objects.create(
            name='The Depot')
        self.user = self.create_user(self.depot, 'Thomas Test')

        self.purchase_datetime = timezone.make_aware(
            datetime(2021, 10, 15, 15, 34)
        )

        self.invoice_datetime = timezone.make_aware(
            datetime(2021, 10, 31, 12, 30)
        )

        self.items = self.create_test_items()

    # utility methods
    def create_user(self, depot, name):

        user = UserProfile.objects.create(
            username=name,
            first_name='Benno',
            last_name=name,
            street='Teststrasse 121',
            zip='8049',
            city='Zürich',
            depot=depot
        )
        user.save()

        return user

    def create_test_items(self):
        # create a group
        self.itemgroup = ItemGroup.objects.create(
            idx=1,
            name='Item Group'
        )
        self.itemgroup.save()

        # create 2 items
        item1 = Item.objects.create(
            code=123,
            name='Item 123',
            group=self.itemgroup,
            depot=self.depot,
            price=1.20
        )
        item1.save()

        item2 = Item.objects.create(
            code=456,
            name='Item 456',
            group=self.itemgroup,
            depot=self.depot,
            price=4.50
        )
        item2.save()

        return [item1, item2]

    def create_purchase(self, depot, user, datetime, items):

        purchase = Purchase.objects.create(
            user=user,
            depot=depot,
            datetime=datetime
        )
        purchase.save()

        for item in items:
            i_p = ItemPurchase.objects.create(
                depot=depot,
                user=user,
                purchase=purchase,
                item=item,
                quantity=1,
                price=item.price
            )
            i_p.save()

        return purchase


class InvoiceTest(InvoiceTestBase):

    def test_get_billable_purchases(self):
        self.create_purchase(
            self.depot, self.user, self.purchase_datetime,
            self.items
        )

        no_purchases = get_billable_purchases(
            self.depot,
            self.purchase_datetime + timedelta(days=-1)
        )

        self.assertEquals(0, len(no_purchases))

        some_purchases = get_billable_purchases(
            self.depot,
            self.purchase_datetime + timedelta(days=1)
        )

        # we should get a dictionary with 1 purchase for 1 user
        self.assertEquals(1, len(some_purchases.keys()))
        self.assertEquals(1, len(some_purchases.values()))

    def test_create_invoice(self):
        # create 2 item purchases
        itm_p1= ItemPurchase(
            depot=self.depot,
            user=self.user,
            item=self.items[0],
            quantity=2,
            price=self.items[0].price
        )
        itm_p1.save()
        itm_p2 = ItemPurchase(
            depot=self.depot,
            user=self.user,
            item=self.items[1],
            quantity=1,
            price=self.items[1].price
        )
        itm_p2.save()
        
        invoice = create_invoice(
            self.depot, self.user, self.invoice_datetime,
            [itm_p1, itm_p2]
            )
        
        self.assertEquals(self.depot, invoice.depot)
        self.assertEquals(self.user, invoice.user)
        self.assertEquals(2, len(invoice.itempurchases.all()))
        expected_amount = Decimal(f'{2 * self.items[0].price + self.items[1].price:.2f}')
        self.assertEquals(expected_amount, invoice.amount)


class InvoiceTestsMultiUsers(InvoiceTestBase):
    def setUp(self):
        super().setUp()

        self.user2 = self.create_user(self.depot, 'Hans Muster')

        self.purchase1 = self.create_purchase(
            self.depot, self.user, self.purchase_datetime,
            self.items
        )

        self.purchase2 = self.create_purchase(
            self.depot, self.user, self.purchase_datetime,
            self.items[0:1]
        )

        self.purchase3 = self.create_purchase(
            self.depot, self.user2, self.purchase_datetime,
            self.items
        )

    def test_get_billable_purchases_multiple_user(self):

        billables = get_billable_purchases(self.depot, self.purchase_datetime)

        # we should get dictionary for 2 users
        self.assertEquals(2, len(billables))

        # self.user has 2 purchases, user2 has 1
        self.assertEquals(2, len(billables[self.user]))
        self.assertEquals(1, len(billables[self.user2]))

    def test_create_invoice(self):
        invoice = create_invoice_from_purchases(
            self.depot, self.user, self.invoice_datetime,
            [self.purchase1, self.purchase2])

        self.assertEquals(Decimal('6.9'), invoice.amount)
        self.assertEquals(self.invoice_datetime, invoice.date)
        # purchase1 has 2 items, purchase2 1
        self.assertEquals(3, len(invoice.itempurchases.all()))

    def test_create_invoices(self):
        invoices = create_invoices(
            self.depot, self.invoice_datetime, self.invoice_datetime)

        self.assertEquals(2, len(invoices))

        self.assertEquals(self.user, invoices[0].user)
        self.assertEquals(Decimal('6.9'), invoices[0].amount)

        self.assertEquals(self.user2, invoices[1].user)
        self.assertEquals(Decimal('5.7'), invoices[1].amount)
