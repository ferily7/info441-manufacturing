from django.shortcuts import render

# Create your views here.
def homepage(request):
	content = {}
	if request.user.is_authenticated:
		content = {'user':request.user}

	return render(request, "index.html", content)

def loginpage(request):
	return render(request, "auth/signin.html", {})

def registerpage(request):
	return render(request, "auth/register.html", {})
