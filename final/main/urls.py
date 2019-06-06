from django.conf.urls import url
from . import views

#These two added for viewsets
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('cart/<int:user_id>', 
        views.CartView.as_view(), name='cart'),
    path('spec/<int:spec_id>', 
        views.SpecDocView.as_view(), name='spec_id'),
    url(r'^spec', views.AllSpecView.as_view()),
    url(r'^cart', views.CreateCartView.as_view()),
]
