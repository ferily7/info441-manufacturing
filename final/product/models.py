from django.db import models
from auth.models import User

# This creates the product model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=250, blank=True)
    quantity = models.IntegerField(default=False, blank=True)
    price = models.FloatField(null=True, blank=True)
    product_type = models.ManyToManyField(ProductType, related_name="product_type", blank=True)
    seller = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="seller")
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Only set added_by during the first save.
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.CharField(max_length=250, blank=True)

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, 
        null=True, blank=True, on_delete=models.SET_NULL, related_name="seller")
    rating = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, blank=True)
