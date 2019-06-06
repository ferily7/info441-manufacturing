from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
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

        return render(request, 'product/productHome.html', {'products': allSerializer.data,
            'user': request.user, 'isBuyer':isBuyer, 'form': forms.ProductForm()})

    def post(self, request, format=None):
        """ This creates a new product based on the request"""

        # Checks if the user is logged in
        if not request.user.is_authenticated:
            messages.error(request, 'Not logged in')
            return HttpResponseRedirect('/')

        newProduct = models.Product.objects.create(name=request.data["name"],
            description=request.data["description"],
            stock=request.data["stock"],
            price=request.data["price"],
            seller=request.user
        )
        newProduct.save()
        messages.success(request, 'Successfully created product')
        return HttpResponseRedirect('/product')

class ProductView(APIView):
    def post(self, request, format=None, product_id=0):
        """ This deletes the product based on the given product id """

        if not request.user.is_authenticated:
            return Response("Not logged in", status.HTTP_401_UNAUTHORIZED)

        product = models.Product.objects.get(id=product_id)

        # Checks to see if the user is the seller of the product based on the product id
        if product.seller != request.user:
            messages.error(request, 'Forbidden, not creator of product')
            return HttpResponseRedirect('/product')

            # return Response("Forbidden, not creator of review", status.HTTP_403_FORBIDDEN)

        # Deletes the product
        product.delete()
        messages.success(request, 'Product deleted.')
        return HttpResponseRedirect('/product')

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