from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('customer-list/', views.CustomerListView.as_view(), name='customer-list'),
    # path('customer-search/', views.CustomerSearchView.as_view(), name='customer-search'),
    path('customer-detail/<str:username>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
    path('profile/update/', views.UserUpdateProfileView.as_view(), name='update_profile'),
]
