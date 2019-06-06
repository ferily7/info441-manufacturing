from django.contrib import admin
from .models import Brand, Cart, SpecDoc, ProductCart
# Register your models here.

admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(SpecDoc)
admin.site.register(ProductCart)
