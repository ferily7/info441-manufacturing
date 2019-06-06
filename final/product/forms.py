from django import forms

class ReviewForm(forms.Form):
    rating = forms.CharField(label='Rating', max_length=5)
    description = forms.CharField(widget=forms.Textarea, max_length=250)

class BrandForm(forms.Form):
    name = forms.CharField(label='Brand name', max_length=22)
    description = forms.CharField(widget=forms.Textarea, max_length=250)

class ProductForm(forms.Form):
    name = forms.CharField(label='Product name', max_length=22)
    description = forms.CharField(widget=forms.Textarea, max_length=250)
    stock = forms.IntegerField()
    price = forms.DecimalField(max_digits=7, decimal_places=2)