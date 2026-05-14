from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.email_login_request, name='email-login'),
    path('login/confirm/<uidb64>/<token>/', views.email_login_confirm, name='email-login-confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('basket/new/', views.new_basket, name='new-basket'),
    path('basket/<int:basket_id>/', views.show_basket, name='show-basket'),
    path('basket/<int:basket_id>/choose-article/', views.choose_article, name='choose-article'),
    path('basket/<int:basket_id>/create-purchase/<int:article_id>/', views.create_purchase, name='create-purchase'),
    path('basket/<int:basket_id>/finish-basket/', views.finish_basket, name='finish-basket'),
    path('purchase/<int:purchase_id>/inc-quantity/', views.inc_quantity, name='inc-quantity'),
    path('purchase/<int:purchase_id>/dec-quantity/', views.dec_quantity, name='dec-quantity'),
    path('purchase/<int:purchase_id>/delete/', views.delete_purchase, name='delete-purchase'),
    path('invoice/pdf/<id>', views.invoice_pdf, name='invoice-pdf'),
    path('articlelist', views.articles_pdf, name='articles-pdf'),
]
