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

class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    product_type = ProductTypeSerializer()

    class Meta:
        model = models.Product
        fields = (
            "id",
            "name",
            "description",
            "quantity",
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

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer()

    class Meta:
        model = models.Review
        fields = (
            "id",
            "reviewer",
            "rating",
            "description",
        )

        read_only_fields = (
            "id",
            "reviewer",
        )
