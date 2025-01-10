from rest_framework import serializers
from . import models
from product.serializers import MangoSerializer
from product.models import Mango
from django.contrib.auth.models import User
from .models import Cart
from customer.serializers import CustomerSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


class AddToCartSerializer(serializers.ModelSerializer):
    mango = MangoSerializer()
    class Meta:
        model = models.AddToCart
        fields = "__all__"


class CartItemsUpdateSerializer(serializers.ModelSerializer):
#     mango = serializers.PrimaryKeyRelatedField(queryset=Mango.objects.all()) 
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), required=False)

    class Meta:
        model = models.AddToCart
        fields ='__all__'





class OrderSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Order
        fields = '__all__'


class OrderGetSerializer(serializers.ModelSerializer):
    product=MangoSerializer()
    class Meta:
        model = models.Order
        fields = '__all__'