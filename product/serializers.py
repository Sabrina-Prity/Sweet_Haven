from rest_framework import serializers
from . import models



class MangoSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Mango
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Comment
        fields = '__all__'