from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.response import Response

from . import models
from . import permissions as my_permissions
from . import serializers


class PurchaseView(generics.ListCreateAPIView):
    def get_queryset(self):
        my_purchases = models.Purchase.objects \
            .filter(user=self.request.user) \
            .order_by('-datetime')

        return my_purchases

    serializer_class = serializers.PurchaseSerializer
    permission_classes = [my_permissions.MayReadPurchases]


class AvailableItemsView(generics.ListAPIView):
    def get_queryset(self):
        now = timezone.now()
        is_active_query = Q(active_from__lte=now) & (Q(active_until__isnull=True) | Q(active_until__gt=now))

        queryset = models.Item.objects.filter(is_active_query)
        return queryset

    serializer_class = serializers.AvailableItemsSerializer
    permission_classes = [permissions.IsAuthenticated]


class DepotUsersView(generics.ListCreateAPIView):
    def get_queryset(self):
        depot_uuid = self.kwargs['depot_uuid']
        depot = models.Depot.objects.filter(uuid=depot_uuid).first()
        return depot.users.all()

    serializer_class = serializers.DepotUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrentUser(generics.GenericAPIView):
    """
    Simple get-only view returning the currently logged in user.
    Is used by frontend to determine authentication state
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    serializer_class = serializers.DepotUserSerializer
    permission_classes = [permissions.IsAuthenticated]
