from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

path('product/<int:product_id>', views.ProductView.as_view()),
path('product_type/<int:product_id>',  views.ProductTypeView.as_view()),
path('review/<int:review_id>',  views.ReviewView.as_view()),

]