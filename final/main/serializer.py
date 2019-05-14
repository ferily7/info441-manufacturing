from rest_framework import serializers
#from auth.serializers import UserSerializer
#from product.serializers import ProductSerializer
from product.models import Product
from . import models

class BrandSerializer(serializers.ModelSerializer):
    class Meta: 
        model = models.Brand
        fields = (
            "id",
            "name",
            "description"
        )
        read_only_fields = (
            "id",
        )

class CartSerializer(serializers.ModelSerializer):
    #products = ProductSerializer(many=True)

    class Meta:
        model = models.Cart
        field = (
            "id",
            "quantity",
            "total_price",
            "products"
        )
        read_only_fields = (
            "id",
        )

class SpecDocSerializer(serializers.ModelSerializer):
    #creator = UserSerializer()

    #product = ProductSerializer()

    class Meta:
        model = models.SpecDoc
        field = (
            "id",
            "name",
            "description",
            "creator",
            "creator_type",
            "product",
            "content",
            "editedBy"
        )

        read_only_fields = (
            "id",
            "creator",
            "creator_type",
            "product",
        )
