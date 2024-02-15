from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Add any other fields related to your category

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='product_images/')
    # Add any other fields related to your product