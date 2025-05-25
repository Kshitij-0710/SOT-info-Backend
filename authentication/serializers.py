from rest_framework import serializers
from .models import User, RegistrationOTP
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, default='STUDENT')
    password = serializers.CharField(write_only=True)
    ref_name = "AuthUserSerializer" 

    def validate(self, attrs):
        email = attrs.get('email').lower()
        user_type = attrs.get('user_type')

        # Check for unique (email, user_type) pair
        if User.objects.filter(email=email, user_type=user_type).exists():
            raise serializers.ValidationError("This email is already registered with the selected user type.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data['email'].lower()
        user_type = validated_data['user_type'].upper()

        # Create the user
        user = User(
            email=email,
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            user_type=user_type,
        )
        user.set_password(password)

        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    
    def validate(self, data):
        try:
            registration_otp = RegistrationOTP.objects.filter(
                email=data['email']
            ).order_by('-created_at').first()
            
            if not registration_otp:
                raise serializers.ValidationError("No registration request found for this email.")
            
            if not registration_otp.is_valid():
                raise serializers.ValidationError("OTP has expired. Please register again.")
            
            if registration_otp.code != data['otp']:
                raise serializers.ValidationError("Invalid OTP.")
            
            data['registration_data'] = registration_otp
            return data
        except RegistrationOTP.DoesNotExist:
            raise serializers.ValidationError("No registration request found for this email.")

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')
        user_type = data.get('user_type').upper()

        username_id = f"{email}__{user_type}"
        user = authenticate(username=username_id, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials for this user type.")

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone_number', 'user_type', 'date_joined']
        read_only_fields = ['date_joined']
