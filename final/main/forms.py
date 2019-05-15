from django import forms

class BrandForm(forms.Form):
    name = forms.CharField(label='Brand name', max_length=22)
    description = forms.CharField(widget=forms.Textarea, max_length=250)
