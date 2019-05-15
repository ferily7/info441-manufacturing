from django import forms
from . import models


class RegistrationForm(forms.Form):

    # Registration fields
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, widget=forms.PasswordInput())
    passwordconf = forms.CharField(label='Password Confirmation', max_length=30, required=True, widget=forms.PasswordInput())
    email = forms.CharField(label='Email', max_length=30, required=True)

    BUYER = 'BU'
    SELLER = 'SE'
    MANUFACTURER = 'MA'
    TYPE_CHOICES = (
        (BUYER, 'BUYER'),
        (SELLER, 'SELLER'),
        (MANUFACTURER, 'MANUFACTURER'),
    )
    account_type = forms.ChoiceField(choices=TYPE_CHOICES, required=True)

    street_address = forms.CharField(label='Street Address', max_length=100, required=True)
    city = forms.CharField(label='City', max_length=50, required=True)
    state = forms.CharField(label='State', max_length=50, required=True)
    zipcode = forms.IntegerField(label='Zipcode', min_value=0, required=True)
    


class SignInForm(forms.Form):

    # Sign in fields
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, widget=forms.PasswordInput())