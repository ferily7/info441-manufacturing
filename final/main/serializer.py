from rest_framework import serializers
from auth.serializers import UserSerializer
from product.serializer import ProductSerializer
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
    products = ProductSerializer(many=True)
    buyer = UserSerializer()
    class Meta:
        model = models.Cart
        fields = (
            "id",
            "quantity",
            "total_price",
            "products",
            "buyer"
        )
        read_only_fields = (
            "id",
        )

class SpecDocSerializer(serializers.ModelSerializer):
    creator = UserSerializer()

    product = ProductSerializer()

    class Meta:
        model = models.SpecDoc
        fields = (
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

class ProductCartSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    
    #cart_id = CartSerializer()
    class Meta:
        model = models.ProductCart
        fields = (
            "id",
            "product_id",
            "quantity"
        )
        read_only_fields = (
            "id",
        )
