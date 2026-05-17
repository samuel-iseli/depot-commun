from decimal import Decimal
from io import BytesIO

from django.contrib.auth import get_user_model
from django.utils import timezone

from store.tests.test_invoice import InvoiceTestBase
from store.models import Purchase, Settings, ShoppingBasket
from store.billing import create_invoice
from store.invoice_pdf import InvoicePdfRenderer


class InvoicePdfTest(InvoiceTestBase):
    def test_generate_invoice_pdf(self):
        settings = Settings.get_solo()
        settings.payment_account_number = 'CH9300762011623852957'
        settings.payment_account_name = 'Depot Commun'
        settings.payment_account_street = 'Siedlung Kraftwerk1'
        settings.payment_account_house_number = '1'
        settings.payment_account_postal_code = '8049'
        settings.payment_account_place = 'Zuerich'
        settings.save()

        total_amount = 1.20 + 2 * 4.5

        # 1x item0, 2x item1
        ip1 = Purchase(
            article=self.articles[0], quantity=1,
            price=self.articles[0].price,
            customer=self.customer)
        ip1.save()
        
        ip2 = Purchase(
            article=self.articles[1], quantity=2, price=self.articles[1].price,
            customer=self.customer)
        ip2.save()

        invoice = create_invoice(
            self.customer, self.invoice_datetime,
            [ip1, ip2]
        )
        # test pdf rendering
        # outstream = BytesIO()
        with open('test_invoice.pdf', 'wb') as outstream:
            renderer = InvoicePdfRenderer()
            renderer.render(invoice, outstream)


class InvoiceAppBasketsSectionTest(InvoiceTestBase):
    """Unit tests for render_app_baskets — checks the story elements produced,
    not the visual PDF output."""

    def _story(self, invoice):
        story = []
        InvoicePdfRenderer().render_app_baskets(invoice, story)
        return story

    def setUp(self):
        super().setUp()
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='invoice-basket-user',
            password='test-pass',
        )
        self.customer.users.add(self.user)

    def _paragraph_texts(self, story):
        """Flatten all Paragraph text values from table cells in the story."""
        from reportlab.platypus import Table, Paragraph
        texts = []
        for elem in story:
            if isinstance(elem, Paragraph):
                texts.append(elem.text)
            elif isinstance(elem, Table):
                for row in elem._cellvalues:
                    for cell in row:
                        if isinstance(cell, Paragraph):
                            texts.append(cell.text)
        return texts

    def test_no_baskets_no_direct_produces_empty_story(self):
        invoice = create_invoice(self.customer, self.invoice_datetime, [])
        self.assertEqual(self._story(invoice), [])

    def test_basket_row_shows_count_and_total(self):
        invoice = create_invoice(self.customer, self.invoice_datetime, [])
        basket = ShoppingBasket.objects.create(
            customer=self.customer,
            user=self.user,
            invoice=invoice,
            completed=timezone.now(),
        )
        Purchase.objects.create(
            article=self.articles[0], quantity=2,
            price=Decimal('1.20'), customer=self.customer, basket=basket,
        )
        Purchase.objects.create(
            article=self.articles[1], quantity=1,
            price=Decimal('4.50'), customer=self.customer, basket=basket,
        )

        texts = self._paragraph_texts(self._story(invoice))
        self.assertIn('2', texts)
        self.assertIn('6.90', texts)

    def test_direct_purchase_adds_tallied_on_paper_row(self):
        direct = Purchase.objects.create(
            article=self.articles[0], quantity=1,
            price=Decimal('1.20'), customer=self.customer,
        )
        basket = ShoppingBasket.objects.create(
            customer=self.customer,
            user=self.user,
            completed=timezone.now(),
        )
        invoice = create_invoice(self.customer, self.invoice_datetime, [direct], baskets=[basket])

        texts = self._paragraph_texts(self._story(invoice))
        self.assertIn('Artikel auf Papier erfasst', texts)

    def test_no_tallied_row_when_only_baskets(self):
        invoice = create_invoice(self.customer, self.invoice_datetime, [])
        basket = ShoppingBasket.objects.create(
            customer=self.customer, user=self.user, invoice=invoice, completed=timezone.now(),
        )
        Purchase.objects.create(
            article=self.articles[0], quantity=1,
            price=Decimal('1.20'), customer=self.customer, basket=basket,
        )

        texts = self._paragraph_texts(self._story(invoice))
        self.assertNotIn('Artikel auf Papier erfasst', texts)
