from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    # create a product model with a name, a description, and a price fields
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # return the name of the product as the string representation
        return self.name



# app/models.py
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # Add fields for shipping information as needed
    shipping_name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=200)


class OrderItem(models.Model):
    # create an order item model with an order, a product, a quantity and a price fields
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


