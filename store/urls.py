from django.urls import include, path
from . import views

app_name = 'store'

urlpatterns = [
    path('', include('store.urls_frontend')),
    path('invoice/pdf/<id>', views.invoice_pdf, name='invoice-pdf'),
    path('articlelist', views.articles_pdf, name='articles-pdf')
]
