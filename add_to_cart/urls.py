from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('cart', views.AddToCartViewSet, basename='cart')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('order-history', views.OrderHistoryViewSet, basename='order-history')
router.register('admin/orders', views.AdminOrderViewSet, basename='admin-orders')
urlpatterns = [
    path('', include(router.urls)),
]