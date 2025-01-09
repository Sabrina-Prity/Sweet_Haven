from rest_framework import viewsets
from .models import Mango, Comment
from .serializers import MangoSerializer, CommentSerializer
from rest_framework import filters, pagination
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from category.models import Category
from . import serializers


class MangoPagination(pagination.PageNumberPagination):
    page_size = 6 #ek page e koita item thakbe
    page_size_query_param = page_size
    max_page_size = 100

class MangoViewSet(viewsets.ModelViewSet):
    queryset = Mango.objects.all()
    serializer_class = MangoSerializer
    permission_classes = [AllowAny]
    # pagination_class = MangoPagination
    # permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'category__name']

    def perform_create(self, serializer):
        category_id = self.request.data.get('category')
        if category_id:
            category = Category.objects.get(id=category_id)
            serializer.save(category=category)
        else:
            # Handle the case where category is missing (maybe throw an error or set default)
            raise serializers.ValidationError('Category is required.')






class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], url_path='comments_by_mango')
    def comments_by_mango(self, request):
        mango_id = request.query_params.get('mango_id', None)
        
        if mango_id is not None:
            comments = Comment.objects.filter(mango_id=mango_id)  
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Mango ID is required."}, status=400)
    
    def perform_create(self, serializer):
        user = self.request.user  
        mango_id = self.request.data.get('mango')
        if not mango_id:
            raise ValidationError("Mango ID is required.")
        serializer.save(user=user, mango_id=mango_id)

    def get_queryset(self):
        queryset = super().get_queryset()
        mango_id = self.request.query_params.get('mango_id')
        if mango_id:
            queryset = queryset.filter(mango_id=mango_id)
        return queryset