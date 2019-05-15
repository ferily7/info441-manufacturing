from django.shortcuts import render, redirect
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from . import models, serializer, forms
from product.models import Product

class BrandView(APIView):
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
    def get(self, request, cart_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart_id = self.kwargs['cart_id']
        cart = models.Cart.objects.get(id=cart_id)

        serialized_cart = serializer.CartSerializer(cart)

        return Response(serialized_cart.data)

    def post(self, request, cart_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart_id = self.kwargs['cart_id']
        cart = models.Cart.objects.get(id=cart_id)

        product = Product.objects.get(id=request.data['id'])
        
        cart.products.add(product)
        cart.save()

        return Response("Product successfully added to cart.")

    def delete(self, request, cart_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        cart_id = self.kwargs['cart_id']
        cart = models.Cart.objects.get(id=cart_id)

        cart.products.remove(request.data)
        cart.save()

        return Response("Product successfully deleted.")

class SpecDocView(APIView):
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
    def get(self, request, format=None):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        specs = models.SpecDoc.objects.all()
        serialized_specs = serializer.SpecDocSerializer(specs, many=True)

        return Response(serialized_specs.data)
