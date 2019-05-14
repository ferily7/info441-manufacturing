from django.conf.urls import url
from . import views

#These two added for viewsets
from django.urls import path
from django.conf.urls import include

url_patterns = [
    url(r'^brand', 
        views.BrandView.as_view()),
    path('cart/<int:cart_id>', 
        views.CartView.as_view()),
    path('spec/<int:spec_id>', 
        views.SpecDocView.as_view()),
    url(r'^spec', views.AllSpecView.as_view()),
]
