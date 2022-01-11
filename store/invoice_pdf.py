import datetime
from collections import defaultdict
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.utils.formats import get_format
from django.utils.dateformat import format
from django.utils.translation import gettext as _
from .models import Settings
# from svglib.svglib import SvgRenderer
# from lxml import etree


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

        # build the pdf document
        doc = SimpleDocTemplate(outfile)
        doc.build(
            story,
            onFirstPage=self.draw_payslip,
            onLaterPages=self.draw_payslip)

    def render_addresses(self, invoice, story):
        """
        render table with addresses
        """
        addr = self.get_own_address()

        lines = [
            addr['name'],
            addr['street'],
            '%s %s' % (addr['zip'], addr['city'])
        ]

        if addr.get('extra_line', ''):
            lines.insert(1, addr['extra_line'])

        org_address = Paragraph(
            '<br/>'.join(lines),
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
        title = Paragraph('Rechnung Nr %d' % invoice.id, self.heading1)
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

        for (article, price), quantity in article_lines.items():
            lines.append((
                Paragraph(article.name, self.normal),
                Paragraph(str(quantity), self.normalright),
                Paragraph('%5.2f' % price, self.normalright),
                Paragraph('%10.2f' % (quantity * price), self.normalright)
                ))
        lines.append((
            Paragraph('<b>Total</b>', self.normal),
            Paragraph(''),
            Paragraph(''),
            Paragraph('<b>%10.2f</b>' % invoice.amount, self.normalright)))

        items_table = Table(lines, (None, 2 * cm, 2 * cm, 2 * cm), style=self.table_style)
        story.append(items_table)

    def render_paymentinfo(self, story):
        settings = Settings.get_solo()

        story.append(
            Paragraph('Bitte einzahlen mit Angabe von Rechnungsnummer auf:', self.text)
        )

        lines = (
            settings.payment_bank,
            settings.payment_account_number,
            settings.payment_account_name
        )
        story.append(
            Paragraph('<br/>'.join(lines), self.text)
        )

    def render_payslip(self, bill, story):
        """
        render payslip part with QR-Code
        the payslip is produced into a reporlab
        drawing, which is actually rendered by
        the page render function draw_payslip.
        """
        settings = Settings.objects.first()
        addr = Config.organisation_address()

        payment_type = settings.default_paymenttype
        if is_qr_iban(payment_type.iban):
            qr_svg = get_qrbill_svg(bill, payment_type)
            svg_element = etree.fromstring(qr_svg)

            renderer = SvgRenderer("")

            # save payslip drawing and
            # offset bottom margin
            self.qrpayslip_drawing = renderer.render(svg_element)
            self.bottom_margin = self.qrpayslip_drawing.height
        else:
            self.qrpayslip_drawing = None
            self.bottom_margin = 2 * cm

            story.append(Spacer(1, 2 * cm))

            # if no qr payslip, display account info for payment
            story.append(
                Paragraph(
                    _('Please pay specifying bill number to:'),
                    self.text))
            story.append(
                Paragraph(
                    '%s<br/>%s<br/>' % (
                        payment_type.iban,
                        payment_type.name),
                    self.text))
            story.append(
                Paragraph(
                    '%s<br/>%s, %s %s' % (
                        _('in favor of'),
                        addr['name'],
                        addr['zip'],
                        addr['city']),
                    self.text))

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

    def date_format(self, date):
        fmt = get_format('SHORT_DATE_FORMAT', 'de')
        return format(date, fmt)

    def get_own_address(self):
        """
        get the address of the billing party (ourself)
        """
        return {
            'name': 'Depot Comün',
            'extra_line': 'Siedlung Kraftwerk1 Heizenholz',
            'street': 'Regensdorferstrasse 194',
            'zip': '8049',
            'city': 'Zürich'
        }
