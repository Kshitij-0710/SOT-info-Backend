from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from .models import User, RegistrationOTP
from .serializers import (
    UserRegistrationSerializer, 
    OTPVerificationSerializer,
    UserLoginSerializer,
    UserSerializer
)
from .utils import send_otp_email

class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action == 'verify_otp':
            return OTPVerificationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['register', 'verify_otp', 'login']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        name = serializer.validated_data['name']
        phone_number = serializer.validated_data['phone_number']
        user_type = serializer.validated_data['user_type']
        
        # Hash the password for storage
        password = make_password(serializer.validated_data['password'])
        
        # Generate OTP and store registration data temporarily
        otp = RegistrationOTP.generate_otp(email, name, phone_number, user_type, password)
        
        # Send OTP via email
        send_otp_email(email, name, otp.code)
        
        return Response({
            'message': 'Registration initiated. Please check your email for OTP to complete registration.',
            'email': email,
            'user_type': user_type
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        registration_data = serializer.validated_data['registration_data']
        
        # Create the user now that OTP is verified
        user = User.objects.create(
            email=registration_data.email,
            name=registration_data.name,
            phone_number=registration_data.phone_number,
            user_type=registration_data.user_type,
            password=registration_data.password,  # Already hashed during registration
            is_verified=True
        )
        
        # Delete the used registration OTP
        registration_data.delete()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Registration completed successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(email=email, password=password)
        
        if not user:
            return Response(
                {'message': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def resend_otp(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'message': 'Email is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find the existing registration request
        registration_otp = RegistrationOTP.objects.filter(
            email=email
        ).order_by('-created_at').first()
        
        if not registration_otp:
            return Response(
                {'message': 'No registration request found for this email.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate a new OTP
        new_otp = RegistrationOTP.generate_otp(
            registration_otp.email,
            registration_otp.name,
            registration_otp.phone_number,
            registration_otp.user_type,
            registration_otp.password
        )
        
        # Send OTP via email
        send_otp_email(new_otp.email, new_otp.name, new_otp.code)
        
        return Response({
            'message': 'A new OTP has been sent to your email.'
        }, status=status.HTTP_200_OK)