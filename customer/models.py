from django.db import models
from django.contrib.auth.models import User
from product.models import Mango
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,unique=True, on_delete = models.CASCADE)
    image = models.CharField(max_length=100, null=True, blank=True)
    mobile_no = models.CharField(max_length = 12)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

