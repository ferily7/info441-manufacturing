from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from . import models, serializer, forms
from product.serializer import ProductSerializer
from product.models import Product

class CartView(APIView):
    """
    GET:
    Returns all the items in the cart specified

    POST:
    Adds a new product to the cart specified

    DELETE:
    Deletes the specified product from the specified cart
    """
    http_method_names = ['get', 'post', 'patch', 'delete']

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(CartView, self).dispatch(*args, **kwargs)


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
        
        cart_contents = models.ProductCart.objects.filter(cart_id=user_cart.id)
        cart_contents_serialized = serializer.ProductCartSerializer(cart_contents, many=True).data
        
        user_cart_serialized = serializer.CartSerializer(user_cart).data
        products = user_cart_serialized['products']

        index = 0
        for product in products:
            product['num'] = cart_contents_serialized[index]['quantity']
            product['total_price'] = product['price'] * product['num']
            index += 1

        subtotal = 0
        for product in products:
            subtotal += float(product['price']) * product['num']

        subtotal = format(subtotal, '.2f')

        tax = float(subtotal) * .095

        tax = format(tax, '.2f')

        shipping = format(5.00, '.2f')

        grandTotal = float(subtotal) + float(tax) + float(shipping)
        
        grandTotal = format(grandTotal, '.2f')

        return render(request,
            'main/cart.html', 
            {
                'cart':user_cart_serialized,
                'products':products,
                'subtotal':subtotal,
                'tax':tax,
                'shipping':shipping,
                'grandTotal':grandTotal
            })

    def post(self, request, user_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        user_cart = models.Cart.objects.get(buyer=user)
        user_cart_serialized = serializer.CartSerializer(user_cart).data
        products = user_cart_serialized['products']

        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        serialized_product = ProductSerializer(product)

        if(product in products):
            currProduct = models.ProductCart.objects.get(cart_id=user_cart['id'])
            quantity = currProduct['quantity'] + 1
            newProduct = models.ProductCart(cart_id=user_cart, product_id=product, quantity=quantity)
            currProduct.delete()
            newProduct.save()
        else:
            user_cart.products.add(product)
            newProduct = models.ProductCart(cart_id=user_cart, product_id=product, quantity=1)
            user_cart.save()
            newProduct.save()
        return redirect('/main/cart/' + str(user_id))

    def patch(self, request, user_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        user_cart = models.Cart.objects.get(buyer=user)

        updated_cart = serializer.CartSerializer(user_cart, data=request.data, partial=True)

        if (updated_cart.is_valid()):
            updated_cart.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id=0):
        #Checks if user is signed in 
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        #Get current user
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        #Find user's cart
        user_cart = models.Cart.objects.get(buyer=user)

        #Find Product to delete
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        #Delete product
        user_cart.products.remove(product)
        user_cart.save()

        messages.success(request, 'Item has been removed.')
        return redirect('/main/cart/' + str(user_id))

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
        if not request.user.is_authenticated:
            return redirect('/auth/signin')
            
        cart = serializer.CartSerializer(data={'buyer':request.user['id']})
        if(cart.is_valid()):
            cart.save()
        return Response(cart.error, status=status.HTTP_400_BAD_REQUEST)
