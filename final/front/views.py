from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

def homepage(request):
	content = {}
	if request.user.is_authenticated:
		content = {'user':request.user}

	return render(request, "index.html", content)

def loginpage(request):
	return render(request, "auth/signin.html", {})

def registerpage(request):
	return render(request, "auth/register.html", {})

def aboutpage(request):
	return render(request, 'about.html', {})

@csrf_exempt
def contactpage(request):

	if (request.method == 'GET'):
		return render(request, 'contact.html', {})

	if (request.method == 'POST'):
		# return render(request, 'contact.html')
		messages.success(request, 'Thank you for your feedback.')
		return HttpResponseRedirect('contact')