from collections import defaultdict
import io
from reportlab.platypus import (BaseDocTemplate, Image, KeepTogether,
    Paragraph, SimpleDocTemplate, Spacer, Table, Frame, PageTemplate)
from reportlab.platypus.doctemplate import FrameBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.utils.formats import get_format
from django.utils.dateformat import format
from django.utils.translation import gettext as _
import qrcode


def generate_qrcode(code):
    """
    Generate a QR code image for the given code.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img
    

class ArticlesQrPdfRenderer(object):

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

        # header on first page
        self.header_height = 3 * cm

        # article table style
        self.table_style = [
            # left align all cells
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            # valign top all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # reduce top and bottom
            # padding (default is 3)
            # ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 50),
        ]

    def render(self, articles, outfile):
        """
        render list of articles as PDF into a byte file-like output.
        """
        story = []

        self.render_articles(articles, story)

        # build the pdf document
        doc = SimpleDocTemplate(
            outfile,
            title='',
            author='')
        
        doc.build(story)

    def render_articles(self, articles, story):
        ordered_articles = sorted(
            articles,
            key=lambda a: (a.group.idx, a.sortidx, a.name)
        )
        lines = []
        for article in ordered_articles:
            qr_img = generate_qrcode(article.id)
            qr_img_buffer = io.BytesIO()
            qr_img.save(qr_img_buffer, format='PNG')
            qr_img_buffer.seek(0)
            qr_img_rl = Image(qr_img_buffer, 2*cm, 2*cm)
            lines.append([qr_img_rl, Paragraph(article.name, self.heading1)])
        
        table = Table(lines, colWidths=[3*cm, 12*cm])
        table.setStyle(self.table_style)
        story.append(table)
