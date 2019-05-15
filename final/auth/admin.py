from django.contrib import admin
from .models import Purchase, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Purchase)