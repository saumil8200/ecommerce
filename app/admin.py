from django.contrib import admin

from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "quantity_available", "category")

class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user")

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)