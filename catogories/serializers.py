from rest_framework import serializers

from authentication.models import User
from .models import Form,Placement
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
            'id', 'title', 'description', 'team_members', 
            'tech_stack', 'projecturl', 'achivements', 
            'from_date', 'to_date', 'category', 'created_at', 
            'user_type', 'is_top_6', 'is_ongoing', 'user'
        ]
        read_only_fields = ['user_type', 'is_top_6']
class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = ['id', 'title', 'student', 'description', 'package', 'company', 'date', 'created_at']
        read_only_fields = ['created_at']