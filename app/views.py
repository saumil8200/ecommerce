from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        return HttpResponseRedirect(reverse("index"))
    
    quantity = int(request.POST.get("quantity", 1))
    
    # Get or create a cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item = cart.items.filter(product=product).first()
    if cart_item:
        # If the product is already in the cart, update its quantity
        new_quantity = cart_item.quantity + quantity
        if new_quantity <= product.quantity_available:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            messages.error(request, f"Only {product.quantity_available} units available for '{product.name}'.")
    else:
        # If the product is not in the cart, create a new cart item
        if quantity <= product.quantity_available:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        else:
            messages.error(request, f"Only {product.quantity_available} units available for '{product.name}'.")
    
    return HttpResponseRedirect(reverse("view_cart"))


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "app/cart.html", {"cart": cart})


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