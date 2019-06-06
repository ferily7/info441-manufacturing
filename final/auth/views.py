from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegistrationForm, SignInForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models
from rest_framework import status 

from .models import Profile, Purchase
from product.serializer import ProductSerializer
from product.models import Product
from main.serializer import CartSerializer
from main.models import Cart

@csrf_exempt
def register(request):

    """ Registers a new user in the database"""
    if (request.method == 'GET'):
         # Display empty form
        form = RegistrationForm()
        return render(request, 'auth/register.html', {'form':form}, status=200)

    # If user submits the form
    elif (request.method == 'POST'):
        # Get user input from form
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Get user information from form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            passwordconf = form.cleaned_data['passwordconf']
            email = form.cleaned_data['email']
            account_type = form.cleaned_data['account_type']
            street_address = form.cleaned_data['street_address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            # Return error if password and password confirmation do not match
            if (password != passwordconf):
                messages.error(request, 'Passwords did not match.')
                return HttpResponseRedirect('register')

            # if (User.objects.get(username=username) is not None):
            #     messages.error(request, 'Username already taken.')
            #     return HttpResponseRedirect('register')

            try:
                User.objects.get(username=username)
                messages.error(request, 'Username already taken.')
                return HttpResponseRedirect('register')

            except User.DoesNotExist:
                # Register user
                new_user = User.objects.create_user(username=username, password=password, email=email)
                Profile.objects.create(account_type=account_type,
                                    user=new_user,
                                    street_address=street_address,
                                    city=city, state=state,
                                    zipcode=zipcode)
                Cart.objects.create(buyer=new_user,
                                    quantity=0,
                                    total_price=0)
                
                return HttpResponseRedirect('/auth/signin')

        # User is not registered if form is invalid
        else:
            return HttpResponse("Invalid registration request.", status=400)


    return HttpResponse('working', status=200)

@csrf_exempt
@sensitive_post_parameters()
def signin(request):
    """Renders a signin page and signs in an existing user in the database"""
    # If there is nothing submitted
    if (request.method=='GET'):
        form = SignInForm()
        return render(request, 'auth/signin.html', {'form':form}, status=200)

    # If user submits the form
    elif (request.method=='POST'):

        # Get user input from form
        form = SignInForm(request.POST)

        if (form.is_valid()):

            # Get username and password from form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password'] 

            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)
            
            # Login user if there is a user in the database
            if (user is not None):
                login(request, user)
                return render(request, 'index.html', {})
        
            # User cannot login
            else:
                messages.error(request, 'Username and/or password incorrect.')
                return HttpResponseRedirect('signin')

        # User cannot login if form is unvalid
        else:
            return HttpResponse('Bad login form.', status=400)

    # Methods besides GET and POST are not allowed
    return HttpResponse('Method not allowed on auth/signin.', status=405)

@csrf_exempt
@sensitive_post_parameters()
def signout(request):
    """Renders a signout page and signs out the current user"""
    if (request.method == 'GET'):
        # User cannot be logged out if not authenticated
        if (not request.user.is_authenticated):
            return HttpResponse('Not logged in.', status=200)
        # Log out the user
        else:
            logout(request)
            return render(request, 'index.html', {})

    # Only GET requests are allowed for signout
    return HttpResponse('Method not allowed on auth/signout.', status=405)

class PurchaseView(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        """ Get the purchase history for the current user """
        if (not request.user.is_authenticated):
            return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

        # Get the purchase and serialize
        purchase = models.Purchase.objects.all().filter(user_id=request.user.id)
        purchase_serializer = serializers.PurchaseSerializer(purchase, many=True).data

        return render(request, 'auth/purchases.html', {'purchases': purchase_serializer})

    @csrf_exempt
    def post(self, request, format=None):
        """ Saves a new purchase for the current user """
        if (not request.user.is_authenticated):
            return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

        # Get items in cart
        cart_id = request.POST.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        cart_serializer = CartSerializer(cart).data
        user = User.objects.get(id=cart_serializer['buyer']['id'])

        # Create and save new purchase
        new_purchase = Purchase.objects.create(user_id=user,
                                # products=cart_serializer['products'],
                                total_price=cart_serializer['total_price'],
                                total_items=1)
        for product in cart_serializer['products']:
            print(product)
            # print(product.data)
            # product_serializer = ProductSerializer(product)
            product_object = Product.objects.get(name=product['name'])
            
            new_purchase.products.add(product_object)
        new_purchase.save()
        return HttpResponseRedirect('/auth/purchases')

    # @csrf_exempt
    # def delete(self, request, format=None, purchase_id=0):

    #     """ Deletes the current purchase """
    #     try:
    #         if (not request.user.is_authenticated):
    #             return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

    #         purchase_id = self.kwargs['purchase_id']

    #         # Get the purchase and serialize
    #         purchase = models.Purchase.objects.get(id=purchase_id)
            
    #         # Delete the profile from the database
    #         purchase.delete()

    #         return Response('Delete successful.',
    #                         status=status.HTTP_204_NO_CONTENT)

    #     except:

    #         return Response('Bad request.',
    #                         status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):

    @csrf_exempt
    def get(self, request, format=None):
    # def get(self, request, format=None, profile_id=0):

        """ Displays additional information for a user profile """
        try:
            if (not request.user.is_authenticated):
                return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

            # profile_id = self.kwargs['profile_id']

            user = User.objects.get(id=request.user.id)

            profile = models.Profile.objects.get(user=user)
            profile_serializer = serializers.ProfileSerializer(profile).data

            return render(request, 'auth/profile.html', {'profile': profile_serializer})
            # return Response(profile_serializer.data, status=status.HTTP_200_OK)

        except:
            return Response('Bad request.', status=status.HTTP_400_BAD_REQUEST)

    # @csrf_exempt
    # def post(self, request, format=None):

    #     try:
    #         if (not request.user.is_authenticated):
    #             return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

    #     except:
    #         return Response('Bad request.', status=status.HTTP_400_BAD_REQUEST)



    @csrf_exempt
    def patch(self, request, format=None, profile_id=0):

        """ Updates information for the user profile """

        try:
            if (not request.user.is_authenticated):
                return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

            profile_id = self.kwargs['profile_id']
            user = User.objects.get(id=profile_id)

            profile = models.Profile.objects.get(user=user)
            profile_serializer = serializers.ProfileSerializer(profile, data=request.data, partial=True)

            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data, status=status.HTTP_206_PARTIAL_CONTENT,
                            headers={'Content-Type': 'application/json'})

            return Response('Bad request.',
                            status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response('Bad request.',
                            status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def post(self, request, format=None):
        """ Deletes the current profile """
        try:
            if (not request.user.is_authenticated):
                return Response('User is not authenticated.', status=status.HTTP_401_UNAUTHORIZED)

            user = User.objects.get(id=request.user.id)
            profile = models.Profile.objects.get(user=user)
            cart = Cart.objects.get(buyer=user)

            logout(request)

            # Delete all data related to user from the database
            profile.delete()
            user.delete()
            cart.delete()

            return HttpResponseRedirect('../')

        except:
            return Response('Bad request.',
                            status=status.HTTP_400_BAD_REQUEST)
