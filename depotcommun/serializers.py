from rest_framework import serializers, exceptions
from . import models
from . import services


class AvailableItemsSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Article
        fields = ['code', 'name', 'price', 'tags']


class PurchaseSerializer(serializers.ModelSerializer):
    product_nr = serializers.IntegerField(source='article.code', )
    name = serializers.CharField(source='article.name', read_only=True)
    price = serializers.DecimalField(source='article.price', max_digits=7, decimal_places=2, required=False)

    class Meta:
        model = models.Purchase
        fields = ['code', 'name', 'price', 'quantity']


class UserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    uuid = serializers.CharField()
    name = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = models.UserProfile
        fields = ['name', 'user', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        raise AssertionError("Shouldn't get here")

