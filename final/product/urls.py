from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductHomePage.as_view(), name='product'),
    url(r'product_type', views.ProductTypeView.as_view(), name='product_type'),
    path('<int:product_id>', views.ProductView.as_view()),
    path('reviews/<int:product_id>',  views.ReviewView.as_view()),
    url(r'^brand', views.BrandView.as_view(), name='brand')
]