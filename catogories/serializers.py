from rest_framework import serializers

from authentication.models import User
from .models import Form,Placement, Event, EventRegistration
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User data to include in Form responses"""
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'user_type']
        ref_name = "CategoryUserSerializer"
class FormSerializer(serializers.ModelSerializer):
    """Serializer for Form model with nested user data"""
    user = UserSerializer(read_only=True, allow_null=True)
    
    class Meta:
        model = Form
        fields = [
            'id', 'title', 'document','description', 'team_members', 
            'tech_stack', 'projecturl', 'achivements', 
            'from_date', 'to_date', 'category', 'created_at', 
            'user_type', 'is_top_6', 'is_ongoing', 'user'
        ]
        read_only_fields = ['user_type', 'is_top_6']
class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = ['id', 'title', 'student', 'description', 'package', 'top_2', 'company', 'date', 'created_at']
        read_only_fields = ['created_at']

class EventSerializer(serializers.ModelSerializer):
    registered_users = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'location', 'description', 
            'organizer', 'is_featured', 'image_url', 'created_at', 
            'registered_users'
        ]
        read_only_fields = ['id', 'created_at']

    def get_registered_users(self, obj):
        return obj.registrations.count()  # Count of registered users

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'user', 'registered_at']
        read_only_fields = ['id', 'registered_at']