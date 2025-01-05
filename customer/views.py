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
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect



class CustomerViewset(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Customer.objects.filter(user=self.request.user)

    def is_customer(self, request):
        try:
            customer = models.Customer.objects.get(user=request.user)
            return Response({"is_customer": True}, status=status.HTTP_200_OK)
        except models.Customer.DoesNotExist:
            return Response({"is_customer": False}, status=status.HTTP_200_OK)

    def is_customer_status(self, request):
        return self.is_customer(request)



class UserRegistrationApiView(APIView):
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
        return redirect('login')
    else:
        return redirect('register')
    

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)  # Log the user in
                
                # Return token and login status
                return Response({
                    'token': token.key, 
                    'user_id': user.id, 
                    'user_logged_in': True
                })
            else:
                return Response({'error': "Invalid Credential", 'user_logged_in': False})

        return Response(serializer.errors)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # Delete token
            logout(request)  # Log out user
            return Response({"detail": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
        
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
        