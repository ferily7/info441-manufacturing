from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'product_type', views.ProductTypeView.as_view()),
    path('<int:product_id>', views.ProductView.as_view()),
    path('review/<int:review_id>',  views.ReviewView.as_view()),

]