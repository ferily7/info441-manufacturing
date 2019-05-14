from django.db import models
from django.contrib.auth.models import User

# This creates the product type model
class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=250, blank=True)

# This creates the product model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=250, blank=True)
    quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    product_type = models.ManyToManyField(ProductType, related_name="product_type", blank=True)
    seller = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="seller")

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

# This creates the review model
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewer")
    rating = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=250, blank=True)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)
