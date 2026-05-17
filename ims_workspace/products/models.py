from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# ==========================================
# 1. YOUR EXISTING DATABASE MODELS
# ==========================================

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Current Stock: {self.quantity}"


class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    MOVEMENT_CHOICES = [
        (IN, "Stock In (Restock/Return)"),
        (OUT, "Stock Out (Sale/Damage)"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} | {self.quantity}x {self.product.name}"


# ==========================================
# 2. THE NEW AUTOMATION CODE (SIGNALS)
# ==========================================

@receiver(post_save, sender=StockMovement)
def update_stock_balance(sender, instance, created, **kwargs):
    """
    This function triggers automatically every time a StockMovement is saved.
    """
    if created: # Only calculate when a brand-new movement record is created
        # 1. Get or create the live Stock record for this product
        stock, _ = Stock.objects.get_or_create(product=instance.product)
        
        # 2. Adjust the live balance based on the movement type
        if instance.movement_type == StockMovement.IN:
            stock.quantity += instance.quantity
        elif instance.movement_type == StockMovement.OUT:
            # Prevent negative stock before saving
            if stock.quantity < instance.quantity:
                raise ValidationError(f"Not enough stock! Current stock is {stock.quantity}.")
            stock.quantity -= instance.quantity
            
        # 3. Save the updated quantity back to the database
        stock.save()