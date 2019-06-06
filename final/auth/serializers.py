from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from product.models import ProductType

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email')


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = (
            "id",
            "name",
            "description",
        )
        read_only_fields = (
            "id",
        )

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    product_type = ProductTypeSerializer()

    class Meta:
        model = models.Product
        fields = (
            "id",
            "name",
            "description",
            "stock",
            "price",
            "product_type",
            "seller",
        )
        read_only_fields = (
            "id",
            "product_type",
            "seller",
        )

class PurchaseSerializer(serializers.ModelSerializer):

    user_id = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = models.Purchase
        fields = ('id',
                  'user_id',
                  'products',
                  'total_price',
                  'total_items')
        # read_only_fields = ('id')

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = models.Profile
        fields = ('user',
                  'account_type',
                  'street_address',
                  'city',
                  'state',
                  'zipcode')