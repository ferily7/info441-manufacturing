from django.db import models
from django.contrib.auth.models import User

# This creates the product type model
class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=250, blank=True)

# This creates the brand model
class Brand(models.Model):
    name = models.CharField(max_length=22, blank=False)
    description = models.CharField(max_length=250)

# This creates the product model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=250, blank=True)
    stock = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    product_type = models.ForeignKey(ProductType,
        null=True, blank=True, on_delete=models.SET_NULL, related_name="product_type")
    brand = models.ForeignKey(Brand, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="brand")
    seller = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="seller")

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

# This creates the review model
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewer")
    product = models.ForeignKey(Product, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="review_product")
    rating = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=250, blank=True)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)