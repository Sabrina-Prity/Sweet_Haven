from django.shortcuts import render
from rest_framework import viewsets
from . import models
from .models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework import filters, pagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# from rest_framework.permissions import IsAdminUser
# Create your views here.

# class CategoryPagination(pagination.PageNumberPagination):
#     page_size = 5 #ek page e koita item thakbe
#     page_size_query_param = page_size
#     max_page_size = 100

# class CategoryViewset(viewsets.ModelViewSet):
#     queryset = models.Category.objects.all()
#     serializer_class = serializers.CategorySerializer
    # pagination_class = CategoryPagination
    # permission_classes = [IsAdminUser]

class CategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        if pk:  
            try:
                category = Category.objects.get(pk=pk)
                serializer = CategorySerializer(category)
                return Response(serializer.data)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                category.delete()
                return Response({"detail": "Category deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found!"}, status=status.HTTP_404_NOT_FOUND)