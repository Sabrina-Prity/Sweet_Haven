from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from .models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Customer
        fields = '__all__'

       
 


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    mobile_no = serializers.CharField(required=True)
    image = serializers.CharField(max_length=100,required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','mobile_no', 'email', 'password', 'confirm_password','image' ]

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        mobile_no = self.validated_data['mobile_no']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        image = self.validated_data.get('image')
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()

        customer = Customer(
            user=account,
            mobile_no=mobile_no,
            image=image
        )
        customer.save()
        
        return account
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)



class UserUpdateProfileSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError({'error': "Passwords do not match."})
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # Update the User fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance