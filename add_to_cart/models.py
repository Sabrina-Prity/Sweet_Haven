from django.db import models
from django.contrib.auth.models import User
from product.models import Mango
from rest_framework.permissions import BasePermission
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}"

class AddToCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mango = models.ForeignKey(Mango, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Name: {self.mango.name} | Quantity: {self.quantity}"

    def save(self, *args, **kwargs):
        self.price = self.mango.price * self.quantity
        super().save(*args, **kwargs)

    

BUYING_STATUS = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Mango, on_delete=models.CASCADE)
    quantity = models.IntegerField( default=1)
    buying_status = models.CharField(choices=BUYING_STATUS, max_length=10, default="Pending")
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.product.name} on {self.purchased_at}"
    
    class Meta: 
        verbose_name_plural = "Order"




class IsAdminUser(BasePermission):
 
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
