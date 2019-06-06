from django.contrib import admin
from .models import Product, ProductType, Review, Brand

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(Review)
admin.site.register(Brand)
