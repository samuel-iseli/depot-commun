from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

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
    path('items/available-items/', views.AvailableItemsView.as_view()),
    path('depots/<depot_uuid>/users/', views.UsersView.as_view()),
    path('current-user/', views.CurrentUser.as_view()),
    path('auth/', include((auth_patterns, 'rest_framework'))),
    path('invoice/pdf/<id>', views.invoice_pdf, name='invoice-pdf')
]
