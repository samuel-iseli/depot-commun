from rest_framework import serializers, exceptions

from . import models
from . import services


class AvailableItemsSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Item
        fields = ['product_nr', 'name', 'price', 'tags', 'number_of_items_in_stock']


class ItemPurchaseSerializer(serializers.ModelSerializer):
    product_nr = serializers.IntegerField(source='item.product_nr', )
    name = serializers.CharField(source='item.name', read_only=True)
    price = serializers.DecimalField(source='item.price', max_digits=7, decimal_places=2, required=False)

    class Meta:
        model = models.ItemPurchase
        fields = ['product_nr', 'name', 'price', 'quantity']


class PurchaseSerializer(serializers.ModelSerializer):
    items = ItemPurchaseSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    datetime = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Purchase
        fields = ['user', 'datetime', 'items']

    def create(self, validated_data):
        user = validated_data['user']
        purchase_items_data = validated_data['items']

        return services.create_purchase(user, purchase_items_data)


class DepotUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    uuid = serializers.CharField()
    name = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = models.UserProfile
        fields = ['uuid', 'name', 'user']

    def update(self, instance, validated_data):
        raise AssertionError("Shouldn't get here")

    def create(self, validated_data):
        view = self.context['view']
        depot_uuid = view.kwargs['depot_uuid']

        request = self.context['request']
        secret = request.query_params.get('secret')

        if not secret:
            raise exceptions.ValidationError("You must provide a secret to sign up to a depot.")

        depot = models.Depot.objects.filter(uuid__exact=depot_uuid).first()
        if depot.sign_up_secret != secret:
            raise exceptions.ValidationError("The secret provided was wrong.")

        current_user = validated_data['user']

        requested_uuid = validated_data['uuid']
        if current_user.uuid != requested_uuid:
            raise exceptions.PermissionDenied("You cannot sign up other users than yourself.")

        if depot.users.filter(uuid=current_user.uuid).exists():
            raise exceptions.ValidationError("Already signed up to depot")

        depot.users.add(current_user)
        depot.save()

        return current_user





