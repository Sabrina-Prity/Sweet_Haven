from django.shortcuts import render
from . import serializers
from rest_framework import viewsets,status
from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from rest_framework.permissions import IsAdminUser




class UserRegistrationApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):  

        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(user)

            
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"http://127.0.0.1:8000/customer/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:5500/login.html')
    else:
        return redirect('register')
    

class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)  
                
                return Response({
                    'token': token.key, 
                    'user_id': user.id, 
                    "is_admin": user.is_staff,
                })
            else:
                return Response({'error': "Invalid Credential", 'user_logged_in': False})

        return Response(serializer.errors)



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        try:
            request.user.auth_token.delete() 
            logout(request)  # Log out user
            return Response({"detail": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
        

# class CustomerApiView(APIView):
#     serializer_class = serializers.CustomerSerializer

#     def post(self, request):
#         user = request.user  
        
#         data = request.data
#         data['user'] = user.id  

#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             customer = serializer.save()
#             return Response({"message": "Customer created", "customer_id": customer.id}, status=201)
#         return Response(serializer.errors, status=400)


class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        customers = Customer.objects.all()
        serializer = serializers.CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
# class CustomerSearchView(ListAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = serializers.CustomerSerializer
#     filter_backends = [SearchFilter]
#     search_fields = ['user', 'mobile_no']

class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        try:
            customer = Customer.objects.get(user__username=username)
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    # def get(self, request, pk):
    #         customer = Customer.objects.get(pk=pk)
    #         serializer = serializers.CustomerSerializer(customer)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk):
            customer = Customer.objects.get(pk=pk)
            serializer = serializers.CustomerSerializer(customer, data=request.data, partial=True)  # allow partial updates

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def delete(self, request, pk):
            customer = Customer.objects.get(pk=pk)
            customer.delete()
            return Response({"detail": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
       



        
class UserUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = serializers.UserUpdateProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = serializers.UserUpdateProfileSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=200)
        
        return Response(serializer.errors, status=400)
        