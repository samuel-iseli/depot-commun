from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone

from buying.models import Depot, UserProfile, Item, Purchase, ItemPurchase
from buying.models import Invoice

from buying.billing import get_billable_purchases


class InvoiceTests(TestCase):

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

    def test_get_billable_purchases(self):
        purchase = self.create_purchase(
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

    def test_get_billable_purchases_multiple_user(self):
        user2 = self.create_user(self.depot, 'Hans Muster')

        purchase1 = self.create_purchase(
            self.depot, self.user, self.purchase_datetime,
            self.items
        )

        purchase2 = self.create_purchase(
            self.depot, self.user, self.purchase_datetime,
            self.items[0:1]
        )

        purchase3 = self.create_purchase(
            self.depot, user2, self.purchase_datetime,
            self.items
        )

        billables = get_billable_purchases(self.depot, self.purchase_datetime)

        # we should get 3 purchases for 3 users
        self.assertEquals(2, len(billables))

        # self.user has 2 purchases, user2 has 1
        self.assertEquals(2, len(billables[self.user]))
        self.assertEquals(1, len(billables[user2]))

    # utility methods
    def create_user(self, depot, name):

        user = UserProfile.objects.create(
            username=name
        )
        user.save()

        depot.users.add(user)
        depot.save()

        return user

    def create_test_items(self):
        # create 2 items
        item1 = Item.objects.create(
            product_nr=123,
            name='Item 123',
            depot=self.depot,
            price=1.20
        )
        item1.save()

        item2 = Item.objects.create(
            product_nr=456,
            name='Item 456',
            depot=self.depot,
            price=4.50
        )
        item2.save()

        return [item1, item2]

    def create_purchase(self, depot, user, datetime, items):

        # create a purchase with 1 item2 and 2 items2
        purchase = Purchase.objects.create(
            user=user,
            depot=depot,
            datetime=datetime
        )
        purchase.save()

        for item in items:
            i_p = ItemPurchase.objects.create(
                purchase=purchase,
                item=item,
                quantity=1
            )
            i_p.save()

        return purchase

