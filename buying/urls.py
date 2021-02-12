from django.urls import include, path

from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('depots/<depot_uuid>/available-items/', views.AvailableItemsView.as_view()),
    path('depots/<depot_uuid>/users/', views.DepotUsersView.as_view()),
    path('users/<user_uuid>/purchases/', views.PurchaseView.as_view()),
]

