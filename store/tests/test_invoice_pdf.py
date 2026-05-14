from io import BytesIO

from store.tests.test_invoice import InvoiceTestBase
from store.models import Purchase, Settings
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
