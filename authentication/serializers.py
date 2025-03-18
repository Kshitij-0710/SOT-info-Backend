from rest_framework import serializers
from .models import User, RegistrationOTP
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=15)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, default='STUDENT')
    password = serializers.CharField(write_only=True)
    ref_name = "AuthUserSerializer" 
    def validate_email(self, value):
        # Check if email already exists in the User model
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already in use.")
        return value

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    
    def validate(self, data):
        try:
            # Get the temporary registration data with OTP
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone_number', 'user_type', 'date_joined']
        read_only_fields = ['date_joined']