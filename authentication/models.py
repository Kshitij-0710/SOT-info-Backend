from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import random
import string

class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_number, user_type, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            user_type=user_type,
        )
        
        user.set_password(password)
        user.is_verified = True  # Users are created only after verification
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, phone_number, password=None):
        user = self.create_user(
            email,
            name=name,
            phone_number=phone_number,
            user_type='ADMIN',  # Superusers are admins by default
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('STUDENT', 'Student'),
        ('FACULTY', 'Faculty'),
        ('ADMIN', 'Admin'),
    )
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='STUDENT')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)  # Default is True since we only create verified users
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']
    
    def __str__(self):
        return self.email
    
    def is_student(self):
        return self.user_type == 'STUDENT'
    
    def is_faculty(self):
        return self.user_type == 'FACULTY'
    
    def is_admin(self):
        return self.user_type == 'ADMIN'

class RegistrationOTP(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES, default='STUDENT')
    password = models.CharField(max_length=255)  # Will store hashed password
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.email} - {self.code}"
    
    @classmethod
    def generate_otp(cls, email, name, phone_number, user_type, password):
        # Generate a 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        # Set expiry to 10 minutes from now
        expires_at = timezone.now() + timezone.timedelta(minutes=10)
        
        # Delete any existing OTPs for this email
        cls.objects.filter(email=email).delete()
        
        # Create and save the OTP
        otp = cls(
            email=email,
            name=name,
            phone_number=phone_number,
            user_type=user_type,
            password=password,
            code=otp_code,
            expires_at=expires_at
        )
        otp.save()
        
        return otp
    
    def is_valid(self):
        return timezone.now() <= self.expires_at