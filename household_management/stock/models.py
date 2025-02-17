from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    stock_price = models.FloatField(default=0.00)
    category = models.CharField(max_length=50)
    low_stock_threshold = models.IntegerField(default=0)  # ✅ Set a default value
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.quantity} left"


class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

class Budget(models.Model):
    parent = models.OneToOneField(User, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    remaining = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Budget for {self.parent.username}: ${self.remaining}/${self.limit}"