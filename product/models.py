from django.db import models
from django.contrib.auth.models import User
from category.models import Category

# Create your models here.
class Mango(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.CharField(max_length=200, null=True, blank=True)
    
    
    def __str__(self):
       return self.name
    
STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mango = models.ForeignKey(Mango, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by : {self.user.first_name} {self.user.last_name}"