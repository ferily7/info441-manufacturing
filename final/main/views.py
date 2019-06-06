from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from . import models, serializer, forms
from product.models import Product

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

        return render(request, 
            'main/brand.html', 
                {'brand_list':serialized_brands, 
                'form':forms.BrandForm()
                }
            )

    def post(self, request):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serialized_brand = serializer.BrandSerializer(data=request.data)

        if serialized_brand.is_valid():
            serialized_brand.save()
            return redirect('/main/brand/')
        else:
            return Response(serialized_brand.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        newest_brand = models.Brand.objects.latest('id')
        newest_brand.delete()

        return Response("Latest brand successfully deleted.")
        
class CartView(APIView):
    """
    GET:
    Returns all the items in the cart specified

    POST:
    Adds a new product to the cart specified

    DELETE:
    Deletes the specified product from the specified cart
    """
    def get(self, request, user_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        try:
            user_cart = models.Cart.objects.get(buyer=user)
        except models.Cart.DoesNotExist:
            user_cart = None
        
        user_cart_serialized = serializer.CartSerializer(user_cart).data
        products = user_cart_serialized['products']

        return render(request,
            'main/cart.html', 
            {'cart':user_cart_serialized,'products':products})

    def post(self, request, user_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        user_cart = models.Cart.objects.get(buyer=user)

        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        
        user_cart.products.add(product)
        user_cart.save()

        return Response("Product successfully added to cart.")

    def delete(self, request, user_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        user_cart = models.Cart.objects.get(buyer=user)

        user_cart.products.remove(request.data)
        user_cart.save()

        return Response("Product successfully deleted.")

class SpecDocView(APIView):
    """
    GET:
    Returns the page of the specified specification doc

    PATCH:
    Updates the specified spec with new data passed in

    DELETE:
    Deletes the specifed specification doc
    """
    def get(self, request, spec_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        spec_id = self.kwargs['spec_id']
        spec = models.SpecDoc.objects.get(id=spec_id)

        serialized_spec = serializer.SpecDocSerializer(spec).data

        return render(request, 'main/spec.html', {'spec':serialized_spec, 'product':serialized_spec['product']})

    def patch(self, request, spec_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        spec_id = self.kwargs['spec_id']
        spec = models.SpecDoc.objects.get(id=spec_id)

        update_spec = serializer.SpecDocSerializer(spec, data=request.data, partial=True)
        if update_spec.is_valid():
            update_spec.save()
            return Response(update_spec.data, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, spec_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        spec_id = self.kwargs['spec_id']
        spec_doc = models.SpecDoc.objects.get(id=spec_id)
        spec_doc.delete()

        return Response("Deleted Specification Doc. successfully.")

class AllSpecView(APIView):
    """
    GET:
    Returns all of the specification docs
    """
    def get(self, request, format=None):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        specs = models.SpecDoc.objects.all()
        serialized_specs = serializer.SpecDocSerializer(specs, many=True)

        return Response(serialized_specs.data)

class CreateCartView(APIView):
    """
    POST:
    Create a new cart for current user
    """
    def post(self, request):
        cart = serializer.CartSerializer(data={'buyer':request.user['id']})
        if(cart.is_valid()):
            cart.save()
        return Response(cart.error, status=status.HTTP_400_BAD_REQUEST)
