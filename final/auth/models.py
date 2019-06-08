from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=2, default='BU')
    street_address = models.CharField(max_length=100, default='123 University Way')
    city = models.CharField(max_length=50, default='Seattle')
    state = models.CharField(max_length=50, default='WA')
    zipcode = models.PositiveIntegerField(default='98105')


class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product, related_name='all_products', blank=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_items = models.PositiveSmallIntegerField()
