from rest_framework import serializers
from . import models

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AddToCart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Order
        fields = '__all__'