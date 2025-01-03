from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('mango', views.MangoViewSet, basename='mango')
router.register('comment', views.CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    
]