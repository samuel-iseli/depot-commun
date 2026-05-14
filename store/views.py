from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import permission_required
from . import models
from .invoice_pdf import InvoicePdfRenderer
from .articles_pdf import ArticlesPdfRenderer

@permission_required('store.view_invoice', raise_exception=True)
def invoice_pdf(request, id):
    invoice = get_object_or_404(models.Invoice, pk=id)

    filename = "DC Rechnung %d.pdf" % invoice.id
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        f'attachment; filename="{filename}"'

    InvoicePdfRenderer().render(invoice, response)
    return response


@permission_required('store.view_article', raise_exception=True)
def articles_pdf(request):
    """
    generate pdf of all active articles.
    """
    articles = models.Article.objects.filter(active=True)

    filename = "Artikel Liste.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        f'attachment; filename="{filename}"'

    ArticlesPdfRenderer().render(articles, response)
    return response

