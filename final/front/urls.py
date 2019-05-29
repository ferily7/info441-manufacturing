from django.urls import path
from . import views

urlpatterns = [

    path('', views.homepage, name='home'),
    # path('signin/', views.loginpage, name='login'),
    # path('register/', views.registerpage, name='register')

]