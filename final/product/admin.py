from django.contrib import admin
from .models import Product, ProductType, Review

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Review)