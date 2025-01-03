from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters, pagination

# Create your views here.

class CategoryPagination(pagination.PageNumberPagination):
    page_size = 5 #ek page e koita item thakbe
    page_size_query_param = page_size
    max_page_size = 100

class CategoryViewset(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = CategoryPagination