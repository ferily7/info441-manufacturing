from rest_framework import serializers
from auth.serializers import UserSerializer
from . import models

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductType
        fields = (
            "id",
            "name",
            "description",
        )
        read_only_fields = (
            "id",
        )

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

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    product_type = ProductTypeSerializer()
    brand = BrandSerializer()

    class Meta:
        model = models.Product
        fields = (
            "id",
            "name",
            "description",
            "stock",
            "price",
            "product_type",
            "brand",
            "seller",
        )
        read_only_fields = (
            "id",
            "product_type",
            "brand",
            "seller",
        )

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = models.Review
        fields = (
            "id",
            "reviewer",
            "product",
            "rating",
            "description",
        )

        read_only_fields = (
            "id",
            "reviewer",
            "product"
        )
