from django.contrib import admin
from .models import Cart, SpecDoc, ProductCart
# Register your models here.

admin.site.register(Cart)
admin.site.register(SpecDoc)
admin.site.register(ProductCart)
