from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class Cart(models.Model):
    quantity = models.PositiveSmallIntegerField(blank=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    products = models.ManyToManyField(Product, 
        verbose_name="List of products", blank=True)
    buyer = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='buyer')
        
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

class ProductCart(models.Model):
    cart_id = models.ForeignKey(
        Cart,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='CartID'
    )
    product_id = models.ForeignKey(
        Product,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='ProductID'
    )
    quantity = models.PositiveSmallIntegerField(blank=True)

class SpecDoc(models.Model):
    MANUFACTURER = 'MN'
    SELLER = 'SL'
    CUSTOMER = 'CR'

    CREATOR_OF_SPEC_CHOICES = (
        (MANUFACTURER, 'Manufacturer'),
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer'),
    )

    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=250, blank=True)
    creator = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='creator')
    creator_type = models.CharField(
        max_length=2,
        choices=CREATOR_OF_SPEC_CHOICES,
        default=CUSTOMER
        )
    product = models.ForeignKey(Product, 
        null=True, blank=False, 
        on_delete=models.SET_NULL, 
        related_name='product')
    content = models.TextField(max_length=1000, blank=True)
    editedBy = models.DateTimeField(auto_now=True)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

