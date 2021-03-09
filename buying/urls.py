from django.urls import include, path
from . import views
from rest_framework.authtoken import views as token_views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('items/available-items/', views.AvailableItemsView.as_view()),
    path('depots/<depot_uuid>/users/', views.DepotUsersView.as_view()),
    path('users/<id>/purchases/', views.PurchaseView.as_view()),
    path('api-token-auth/', token_views.obtain_auth_token)
]
