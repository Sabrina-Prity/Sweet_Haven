from rest_framework import serializers
from . import models
from customer.serializers import CustomerSerializer


class MangoSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = models.Mango
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    # user = CustomerSerializer()
      
    class Meta:
        model = models.Comment
        fields = '__all__'


    