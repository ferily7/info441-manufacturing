from django.shortcuts import render
from django.contrib.auth.models import User
from . import serializer, models

#Import APIview for viewsets API interface
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductView(APIView):
    def get(self, request, format=None, product_id=0):
        """ This gets the product based on the given product id """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)
 
        # Gets the given product id
        product_id = self.kwargs['product_id']

        try: 
            product = models.Product.objects.get(id=product_id)
        except:
            return Response("Product ID does not exist", status.HTTP_400_BAD_REQUEST)

        productSerializer = serializer.ProductSerializer(product)

        return Response(productSerializer.data)

    def patch(self, request, format=None, product_id=0):
        """ This updates the product's name, description, quantity, or price if the user is the
        seller of the product """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        product = models.Product.objects.get(id=product_id)

        if product.seller != request.user:
            return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)
        
        updatedProduct = serializer.ProductSerializer(product, data=request.data, partial=True)

        if updatedProduct.is_valid():
            updatedProduct.save()
            return Response(updatedProduct.data, headers = {
            'content-type': 'application/json'
        })
        return Response("Bad request", status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, product_id=0):
        """ This deletes the product based on the given product id """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        product = models.Product.objects.get(id=product_id)

        # Checks to see if the user is the seller of the product based on the product id
        if product.seller != request.user:
            return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)

        # Deletes the product
        product.delete()
        return Response("Successfully deleted product.", status=status.HTTP_204_NO_CONTENT)

class ProductTypeView(APIView):
    def get(self, request, format=None):
        """ This gets all of the current product types """
        
        # This gets all of the users who is registered
        allProductType = models.ProductType.objects.all()
        allSerializer = serializer.ProductTypeSerializer(allProductType, many=True)
        return Response(allSerializer.data)

    def post(self, request, format=None):
        """ This creates a new product type based on name and description """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        productTypeSerializer = serializer.ProductTypeSerializer(data=request.data, context={'request': request})
        
        if productTypeSerializer.is_valid():
            productTypeSerializer.save()
            return Response(productTypeSerializer.data, status=status.HTTP_201_CREATED)
       
        return Response(productTypeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, format=None):
        """ This deletes the most recent product type in the list """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        recentProductType = models.ProductType.objects.latest('id')
        recentProductType.delete()

class ReviewView(APIView):
    def get(self, request, format=None, review_id=0):
        """ This gets the review based on the given review id """

        # Checks if the user is logged in
        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)
 
        # Gets the given review id
        review_id = self.kwargs['review_id']

        try: 
            review = models.Review.objects.get(id=review_id)
        except:
            return Response("Review ID does not exist", status.HTTP_400_BAD_REQUEST)

        reviewSerializer = serializer.ReviewSerializer(review)

        return Response(reviewSerializer.data)

    def patch(self, request, format=None, review_id=0):
        """ This updates the review's rating or description if the user is the creator of 
        the review """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        review = models.Review.objects.get(id=review_id)

        # Checks to see if the user is the person who created the review based on the review id
        if review.reviewer != request.user:
            return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)
        
        # Updates the review based on the given information, the rating number or description
        updatedReview = serializer.ReviewSerializer(review, data=request.data, partial=True)

        if updatedReview.is_valid():
            # Update and saves the review
            updatedReview.save()
            return Response(updatedReview.data, headers = {
            'content-type': 'application/json'
        })
        return Response("Bad request", HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None, review_id=0):
        """ This deletes the review based on the given review id """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        review = models.Review.objects.get(id=review_id)

        # Checks to see if the user is the person who created the review based on the review id
        if review.reviewer != request.user:
            return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response("Successfully deleted review.", status=status.HTTP_204_NO_CONTENT)
