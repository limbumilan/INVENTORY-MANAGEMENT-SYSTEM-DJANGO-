from django.db import models
from products.models import Product # Import your Product model so we can link them

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # This creates a link table behind the scenes connecting Suppliers and Products
    products = models.ManyToManyField(Product, related_name="suppliers", blank=True)

    def __str__(self):
        return self.name