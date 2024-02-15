from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("<int:product_id>", views.product, name="product"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="add_to_cart"),
    path("view-cart", views.view_cart, name="view_cart"),
]