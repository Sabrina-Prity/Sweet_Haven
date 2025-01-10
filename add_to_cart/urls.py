from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()

# router.register('cart/<int:pk>/', views.AddToCartViewSet, basename='cart')
router.register('orders/', views.OrderViewSet, basename='orders')
router.register('order-history/', views.OrderHistoryViewSet, basename='order-history')
# router.register('admin/orders/', views.AdminOrderViewSet, basename='admin-orders')
urlpatterns = [

    path('', include(router.urls)),
    path('cart_create/', views.CartApiView.as_view()),
    path('cart_details/<int:pk>/', views.CartDetails.as_view()),
    path('product_get/', views.ProductGetCartID.as_view()),
    path('cart_products/<int:cart_id>/', views.CartProductsAPIView.as_view(), name='cart-products'),
    path('update-cart-item/<int:pk>/', views.CartItemsUpdate.as_view(), name='cart-item-update'),
    path('orders-view/', views.UserOrdersView.as_view(), name='user-orders'),
    path('specific-order/<int:pk>/', views.UserSpecificOrderView.as_view(), name='specific-order'),
    path('admin-order/', views.AdminOrderAPIView.as_view(), name='admin-order'),
    path('admin-order-updated/<int:pk>/', views.AdminOrderUpdateAPIView.as_view(), name='admin-order-updated'),
    ]