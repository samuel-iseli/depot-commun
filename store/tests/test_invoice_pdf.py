from io import BytesIO

from store.tests.test_invoice import InvoiceTestBase
from store.models import Purchase
from store.billing import create_invoice
from store.invoice_pdf import InvoicePdfRenderer


class InvoicePdfTest(InvoiceTestBase):
    def test_generate_invoice_pdf(self):

        total_amount = 1.20 + 2 * 4.5

        # 1x item0, 2x item1
        ip1 = Purchase(
            item=self.items[0], quantity=1,
            price=self.items[0].price,
            customer=self.customer)
        ip1.save()
        
        ip2 = Purchase(
            item=self.items[1], quantity=2, price=self.items[1].price,
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
