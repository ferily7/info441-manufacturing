from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
# from product.serializers import ProductSerializer
 

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'email')

class PurchaseSerializer(serializers.ModelSerializer):

    user_id = UserSerializer()

    class Meta:
        model = models.Purchase
        fields = ('id',
                  'user_id',
                  'product_id',
                  'total_price',
                  'total_items')
        read_only_fields = ('id')

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