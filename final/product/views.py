from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from auth.models import Profile
from . import serializer, models, forms
from auth.serializers import ProfileSerializer

# Import APIview for viewsets API interface
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductHomePage(APIView):
    def get(self, request, format=None):
        allProducts = models.Product.objects.all()
        allSerializer = serializer.ProductSerializer(allProducts, many=True)
        isBuyer = True

        if request.user.is_authenticated:
            user = Profile.objects.get(user=request.user.id)
            user_serializer = ProfileSerializer(user).data
        
            if (user_serializer['account_type'] == "SE"):
                isBuyer = False
		# content = {'user':request.user, 'isBuyer':isBuyer}


        return render(request, 'product/productHome.html', {'products': allSerializer.data,
            'user_id': request.user.id, 'isBuyer':isBuyer})

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

        # return Response(productSerializer.data)
        return render(request, 'product/product.html', {'product': productSerializer.data})


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

        return render(request, 'product/productType.html', {'type': allSerializer.data})

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
    def get(self, request, format=None, product_id=0):
        """ This gets all the reviews of the product based on the given product id """

        # Gets the given product id
        product_id = self.kwargs['product_id']

        try: 
            allReviews = models.Review.objects.filter(product=product_id)
        except:
            return Response("Product ID does not exist", status.HTTP_400_BAD_REQUEST)

        reviewSerializer = serializer.ReviewSerializer(allReviews, many=True)

        return render(request, 'product/review.html', {'review': reviewSerializer.data,
            'form': forms.ReviewForm(), 'product_id': product_id, 'user': request.user})

    def post(self, request, format=None, product_id=0):
        """ This gets the review the user submitted and saves the review to the given product id """

        # Checks if the user is logged in
        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        product = models.Product.objects.get(id=product_id)
        newReview = models.Review.objects.create(reviewer=request.user,
            product=product,
            rating=request.data["rating"],
            description=request.data["description"]
        )
        newReview.save()
        return redirect('/product/reviews/' + str(product_id))

        # reviewSerializer = serializer.ReviewSerializer(data=newReview)
        # if reviewSerializer.is_valid():
        #     reviewSerializer.save()
        #     return redirect('product/review.html')
        # else:
        #     return Response(reviewSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, format=None, review_id=0):
    #     """ This updates the review's rating or description if the user is the creator of 
    #     the review """

    #     if not request.user.is_authenticated:
    #         return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

    #     review = models.Review.objects.get(id=review_id)

    #     # Checks to see if the user is the person who created the review based on the review id
    #     if review.reviewer != request.user:
    #         return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)
        
    #     # Updates the review based on the given information, the rating number or description
    #     updatedReview = serializer.ReviewSerializer(review, data=request.data, partial=True)

    #     if updatedReview.is_valid():
    #         # Update and saves the review
    #         updatedReview.save()
    #         return Response(updatedReview.data, headers = {
    #         'content-type': 'application/json'
    #     })
    #     return Response("Bad request", HTTP_400_BAD_REQUEST)

    # def delete(self, request, format=None, review_id=0):
    #     """ This deletes the review based on the given review id """

    #     if not request.user.is_authenticated:
    #         return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

    #     review = models.Review.objects.get(id=review_id)

    #     # Checks to see if the user is the person who created the review based on the review id
    #     if review.reviewer != request.user:
    #         return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)

    #     review.delete()
    #     return Response("Successfully deleted review.", status=status.HTTP_204_NO_CONTENT)

class BrandView(APIView):
    """
    GET:
    Returns page with all current brands and a brand registration form

    POST:
    Creates a new brand instance

    DELETE:
    Deletes the latest brand
    """
    def get(self, request, format=None):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        brands = models.Brand.objects.all()
        serialized_brands = serializer.BrandSerializer(brands, many=True).data

        isBuyer = True

        user = Profile.objects.get(user=request.user.id)
        user_serializer = ProfileSerializer(user).data
        
        if (user_serializer['account_type'] == "SE"):
            isBuyer = False

        return render(request, 'product/brand.html', {'brand_list':serialized_brands, 
            'form':forms.BrandForm(), 'isBuyer': isBuyer})

    def post(self, request):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serialized_brand = serializer.BrandSerializer(data=request.data)

        if serialized_brand.is_valid():
            serialized_brand.save()
            return redirect('/product/brand/')
        else:
            return Response(serialized_brand.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        newest_brand = models.Brand.objects.latest('id')
        newest_brand.delete()

        return Response("Latest brand successfully deleted.")