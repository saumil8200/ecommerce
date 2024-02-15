from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "app/app.html", {
        "products": Product.objects.all()
    })

def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, "app/product.html", {
        "product": product,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "app/login.html")

def logout_view(request):
    logout(request)
    return render(request, "app/login.html", {
        "message": "Logged out."
    })