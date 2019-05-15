from django.conf.urls import url
from . import views

#These two added for viewsets
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    url(r'^brand', 
        views.BrandView.as_view(), name='brand'),
    path('cart/<int:cart_id>', 
        views.CartView.as_view()),
    path('spec/<int:spec_id>', 
        views.SpecDocView.as_view(), name='spec_id'),
    url(r'^spec', views.AllSpecView.as_view()),
]
