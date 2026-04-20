from django.urls import path
from django.contrib.auth import views as auth_views

from . import views_frontend

urlpatterns = [
    path('', views_frontend.home, name='home'),
    path('purchase/new/', views_frontend.new_purchase, name='new-purchase'),
    path('purchase/add-article/', views_frontend.add_article, name='add-article'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
