from rest_framework import viewsets
from .models import Mango, Comment
from .serializers import MangoSerializer, CommentSerializer
from rest_framework import filters, pagination



class MangoPagination(pagination.PageNumberPagination):
    page_size = 6 #ek page e koita item thakbe
    page_size_query_param = page_size
    max_page_size = 100

class MangoViewSet(viewsets.ModelViewSet):
    queryset = Mango.objects.all()
    serializer_class = MangoSerializer
    pagination_class = MangoPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price', 'category__name']



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mango_id = self.request.query_params.get('mango_id')
        if mango_id:
            queryset = queryset.filter(mango_id=mango_id)
        return queryset