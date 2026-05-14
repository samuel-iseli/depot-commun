from django.urls import path
from django.contrib.auth import views as auth_views

from . import views_frontend

urlpatterns = [
    path('', views_frontend.home, name='home'),
    path('basket/new/', views_frontend.new_basket, name='new-basket'),
    path('basket/<int:basket_id>/', views_frontend.show_basket, name='show-basket'),
    path('basket/<int:basket_id>/choose-article/', views_frontend.choose_article, name='choose-article'),
    path('basket/<int:basket_id>/create-purchase/<int:article_id>/', views_frontend.create_purchase, name='create-purchase'),
    path('basket/<int:basket_id>/finish-basket/', views_frontend.finish_basket, name='finish-basket'),
    path('purchase/<int:purchase_id>/inc-quantity/', views_frontend.inc_quantity, name='inc-quantity'),
    path('purchase/<int:purchase_id>/dec-quantity/', views_frontend.dec_quantity, name='dec-quantity'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
