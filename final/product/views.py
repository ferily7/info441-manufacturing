from django.shortcuts import render
from django.contrib.auth.models import User
from . import models

#Import APIview for viewsets API interface
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductView(APIView):
    def get(self, request, format=None):
        """ This creates a new channel """

    def post(self, request, format=None):
        """ This creates a new channel """

class ProductTypeView(APIView):
    def get(self, request, format=None, product_id=0):
        """ This creates a new channel """

    def post(self, request, format=None):
        """ This creates a new channel """

class ReviewView(APIView):
    def get(self, request, format=None):
        """ This creates a new channel """

    def post(self, request, format=None):
        """ This creates a new channel """