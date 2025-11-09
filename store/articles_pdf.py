from collections import defaultdict
from reportlab.platypus import (BaseDocTemplate, KeepTogether,
    Paragraph, Spacer, Table, Frame, PageTemplate)
from reportlab.platypus.doctemplate import FrameBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from django.utils.formats import get_format
from django.utils.dateformat import format
from django.utils.translation import gettext as _


class ArticlesPdfRenderer(object):

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
        self.header_height = 2 * cm

        # article table style
        self.table_style = [
            # left align all cells
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            # right aling 2nd column
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            # valign top all cells
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # reduce top and bottom
            # padding (default is 3)
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            # draw box around all cells
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black), 
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), 
        ]


    def render(self, articles, outfile):
        """
        render list of articles as PDF into a byte file-like output.
        """
        story = []

        self.render_header(story)
        self.render_articles(articles, story)

        # build the pdf document
        # to show frame boundaries set showBoundary=1
        doc = BaseDocTemplate(
            outfile,
            title='',
            author='',
            topMargin=1*cm,
            bottomMargin=1*cm)

        # first page, has space for drawing header
        firstPageTemplate = PageTemplate(
            id='First',
            autoNextPageTemplate='Next',
            frames=[
                Frame(doc.leftMargin, doc.bottomMargin+doc.height-self.header_height, doc.width, self.header_height, id='header'),
                Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-self.header_height, id='col1'),
                Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height-self.header_height, id='col2')
            ]
        )

        laterPagesTemplate = PageTemplate(
            id='Next',
            frames=[
                Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height, id='col1'),
                Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height, id='col2')
            ]
        )

        doc.addPageTemplates([firstPageTemplate, laterPagesTemplate])

        doc.build(story)

    def render_header(self, story):
        table = Table(
            [[
                Paragraph('Name', self.heading1),
                Paragraph('E-Mail', self.heading1),
            ]],
            [8*cm, 8*cm],
            )

        story.append(table)
        story.append(FrameBreak())

    def render_articles(self, articles, story):
        ordered_articles = sorted(
            articles,
            key=lambda a: (a.group.idx, a.sortidx, a.name)
        )
        article_groups = defaultdict(list)

        # group by article group
        for a in ordered_articles:
            article_groups[a.group].append(a)

        for group, articles in article_groups.items():
            self.render_article_group(group.name, articles, story)


    def render_article_group(self, groupname, articles, story):
        lines = [
            (article.name, f'{article.price:.2f}', '')
            for article in articles]

        table = Table(lines, [4.3*cm, 1.2*cm, 2.2*cm], style=self.table_style)
        story.append(
            KeepTogether([
                Paragraph(groupname, self.heading2),
                table]))
