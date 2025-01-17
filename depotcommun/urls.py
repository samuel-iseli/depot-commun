from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views
from .api import api

# login dialog using the template from rest_framework
# must to be registered with app_name "rest_framework"
# therefore we need to include these separately
auth_patterns = [
    path('login/', auth_views.LoginView.as_view(
            template_name='rest_framework/login.html',
            redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    # entry path redirects to admin
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    # commented out frontend index.html
    # path('', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('invoicepdf/<id>', views.invoice_pdf, name='invoice-pdf'),
    path('articlespdf', views.articles_pdf, name='articles-pdf'),
    path("api/", api.urls),
]
