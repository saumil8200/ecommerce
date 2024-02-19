from django.urls import path
from . import views

urlpatterns = [
    path("", views.app, name = "app"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register, name = "register"),
    path("<int:product_id>", views.product, name="product"),
    path("categories", views.categories, name="categories"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("view-cart", views.view_cart, name="view_cart"),
    path("view-order", views.view_order, name="view_order")
]