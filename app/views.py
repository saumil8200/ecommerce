from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

from .models import *

# Create your views here.
def app(request):
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

def categories(request):
    return render(request, "app/categories.html", {
        "categories": Category.objects.all(),
    })

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    product = Product.objects.filter(pk=product_id).first()
    if not product:
        return HttpResponseRedirect(reverse("app"))
    
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

    if request.method == 'POST':
        order = Order.objects.create(user=request.user)

        # Transfer cart items to order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

            # Update quantity_available for the product
            product = cart_item.product
            product.quantity_available -= cart_item.quantity
            product.save()

        cart.items.all().delete()

        return redirect(reverse("view_order")) 

    return render(request, "app/cart.html", {"cart": cart})

def view_order(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    
    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user)

    for order in orders:
        order.total_price = sum(item.product.price * item.quantity for item in order.orderitems.all())

    return render(request, "app/order.html", {"orders": orders})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('app')  # Redirect to the home page or any other page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("app"))
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