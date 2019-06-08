from django import forms
from . import models

class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    description = forms.CharField(widget=forms.Textarea, max_length=250)

class BrandForm(forms.Form):
    name = forms.CharField(label='Brand name', max_length=22)
    description = forms.CharField(widget=forms.Textarea, max_length=250)

class ProductForm(forms.Form):
    name = forms.CharField(label='Product name', max_length=22)
    description = forms.CharField(widget=forms.Textarea, max_length=250)
    stock = forms.IntegerField()
    price = forms.DecimalField(max_digits=7, decimal_places=2)
    # product_type = forms.ModelChoiceField(queryset= models.ProductType.objects.all(), to_field_name="name")
    # brand = forms.ModelChoiceField(queryset= models.Brand.objects.all(), to_field_name="name")