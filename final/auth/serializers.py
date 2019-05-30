from rest_framework import serializers
from django.contrib.auth.models import User
# from product.serializer import ProductSerializer
from . import models

 

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email')

class PurchaseSerializer(serializers.ModelSerializer):

    user_id = UserSerializer()
    # products = ProductSerializer()

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