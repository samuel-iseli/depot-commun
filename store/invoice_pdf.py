from collections import defaultdict
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Spacer, Table, Frame, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.utils.formats import get_format
from django.utils.dateformat import format
from .models import Settings
from decimal import Decimal
from qrbill.bill import QRBill
from io import BytesIO, TextIOWrapper
from svglib.svglib import svg2rlg


class InvoicePdfRenderer(object):

    def __init__(self):
        #
        # define styles
        #
        self.org_heading = getSampleStyleSheet()['Heading1']

        self.normal = ParagraphStyle(name='Normal')
        self.normalright = ParagraphStyle(
            'Normal-Right',
            parent=self.normal, alignment=2)
        self.text = ParagraphStyle(
            name='Text',
            parent=self.normal, spaceBefore=6)
        self.heading1 = ParagraphStyle(
            'Heading1',
            parent=self.normal,
            fontName=self.org_heading.fontName,
            fontSize=14, leading=18,
            spaceBefore=12, spaceAfter=6)
        self.heading2 = ParagraphStyle(
            'Heading2', parent=self.normal,
            fontName=self.org_heading.fontName,
            spaceBefore=6, spaceAfter=2)

        self.table_style = [
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # left align all cells
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # valign top all cells
            ('TOPPADDING', (0, 0), (-1, -1), 1),  # reduce top and bottom
            # padding (default is 3)
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (0, -1), 0)  # right align last row
        ]

        self.settings = Settings.get_solo()
        self.qrpayslip_drawing = None

    def render(self, bill, outfile):
        """
        render invoice as PDF in to a byte file-like output.
        """
        story = []

        story.append(Spacer(1, 2 * cm))
        self.render_addresses(bill, story)
        story.append(Spacer(1, 3 * cm))
        self.render_header(bill, story)
        story.append(Spacer(1, 0.5 * cm))
        self.render_items(bill, story)
        story.append(Spacer(1, 1*cm))
        self.render_paymentinfo(story)
        story.append(PageBreak('payslip'))
        story.append(Spacer(1, 10 * cm))

        # pagebreak for payslip page
        self.render_payslip(bill, story)

        # build the pdf document
        # need to set title and author to prevent firefox from
        # displaying "anonymous"
        doc = BaseDocTemplate(
            outfile,
            title='',
            author='')

        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')

        doc.addPageTemplates([
            PageTemplate('invoice', frames=frame),
            PageTemplate('payslip', frames=frame, onPage=self.draw_payslip)
         ])

        doc.build(story)

    def render_addresses(self, invoice, story):
        """
        render table with addresses
        """
        org_address = Paragraph(
            '<br/>'.join([
                'Depot Commün',
                'Siedlung Kraftwerk1 Heizenholz',
            ]),
            self.normal)

        customer = invoice.customer
        memb_address = Paragraph(
            '<br/>'.join([
                customer.name,
                customer.email
            ]),
            self.normal)

        address_table = Table(
            [[org_address, memb_address]],
            style=self.table_style)
        story.append(address_table)

    def render_header(self, invoice, story):
        """
        render title and billing period
        """
        # table with title and date
        title = Paragraph('Rechnung Nr. %d' % invoice.id, self.heading1)
        date = Paragraph(self.date_format(invoice.date), self.normalright)
        title_table = Table([(title, date)], style=self.table_style)
        story.append(title_table)

    def render_items(self, invoice, story):
        """
        render the list of purchases on the bill.
        """
        # group purchases by article and price
        article_lines = defaultdict(lambda: 0)
        for purchase in invoice.purchases.all():
            article = purchase.article
            p_quantity = purchase.quantity
            p_price = purchase.price
            article_lines[(article, p_price)] += p_quantity

        lines = []
        lines.append((
            Paragraph(''),
            Paragraph('<i>Menge</i>', self.normalright),
            Paragraph('<i>Preis</i>', self.normalright),
            Paragraph('<i>Betrag</i>', self.normalright)
        ))

        # add article lines
        for (article, price), quantity in article_lines.items():
            lines.append((
                Paragraph(article.name, self.normal),
                Paragraph(str(quantity), self.normalright),
                Paragraph('%5.2f' % price, self.normalright),
                Paragraph('%10.2f' % (quantity * price), self.normalright)
                ))

        # add extra items
        for itm in invoice.extra_items.all():
            lines.append((
                Paragraph(itm.text, self.normal),
                '', '',
                Paragraph('%10.2f' % itm.amount, self.normalright)
            ))

        lines.append((
            Paragraph('<b>Total</b>', self.normal),
            Paragraph(''),
            Paragraph(''),
            Paragraph('<b>%10.2f</b>' % invoice.amount, self.normalright)))

        items_table = Table(lines, (None, 2 * cm, 2 * cm, 2 * cm), style=self.table_style)
        story.append(items_table)

    def render_paymentinfo(self, story):
        story.append(
            Paragraph('Bitte einzahlen mit Angabe von Rechnungsnummer auf:', self.text)
        )

        lines = (
            self.settings.payment_bank,
            self.settings.payment_account_number,
            self.settings.payment_account_name
        )
        story.append(
            Paragraph('<br/>'.join(lines), self.text)
        )

    def render_payslip(self, invoice, story):
        """
        render payslip part with QR-Code
        the payslip is produced into a reporlab
        drawing, which is actually rendered by
        the page render function draw_payslip.
        """
        bytes_stream = BytesIO()
        wrapper = TextIOWrapper(bytes_stream, encoding='utf8')
        self.get_qrbill_svg(invoice, wrapper)
        
        # save payslip drawing and
        # offset bottom margin
        bytes_stream.seek(0)

        self.qrpayslip_drawing = svg2rlg(bytes_stream)
        self.bottom_margin = self.qrpayslip_drawing.height

    def draw_payslip(self, canvas, document):
        """
        page draw function for drawing the payslip
        at the bottom of the page.
        the payslip drawing has been produced by
        the render_payslip method.
        """
        if self.qrpayslip_drawing is None:
            return

        # draw payslip at the bottom of the page without borders
        canvas.saveState()
        self.qrpayslip_drawing.drawOn(canvas, 0, 0)
        canvas.restoreState()

    def get_qrbill_svg(self, invoice, out_stream):
        """
        Get the QR-Bill payment part as SVG
        """
        qr = QRBill(
            language='de',
            account=self.settings.payment_account_number,
            additional_information="Rechnung %d" % invoice.id,
            amount=Decimal(invoice.amount),
            creditor={
                'name': self.settings.payment_account_name,
                'line1': self.settings.payment_account_street,
                'line2': self.settings.payment_account_place,
                'country': 'CH',
            },
            debtor={
                'name': invoice.customer.name,
                'line1': invoice.customer.street,
                'line2': '%s %s' % (
                    invoice.customer.zip,
                    invoice.customer.city),
                'country': 'CH',
            }
        )
        qr.as_svg(out_stream)

    def date_format(self, date):
        fmt = get_format('SHORT_DATE_FORMAT', 'de')
        return format(date, fmt)
