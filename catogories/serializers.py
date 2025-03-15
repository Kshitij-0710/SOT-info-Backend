from rest_framework import serializers

from authentication.models import User
from .models import Form
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User data to include in Form responses"""
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'user_type']
class FormSerializer(serializers.ModelSerializer):
    """Serializer for Form model with nested user data"""
    user = UserSerializer(read_only=True, allow_null=True)
    
    class Meta:
        model = Form
        fields = [
            'id', 'title', 'description', 'team_members', 
            'tech_stack', 'projecturl', 'achivements', 
            'from_date', 'to_date', 'category', 'created_at', 
            'user_type', 'is_top_6', 'user'
        ]
        read_only_fields = ['user_type', 'is_top_6']
        read_only_fields = ['user_type', 'is_top_6']
    def get_tech_stack_list(self, obj):
        """Returns tech stack as a list for the API"""
        return obj.get_tech_stack_list()
    
    def get_achievements_list(self, obj):
        """Returns achievements as a list for the API"""
        return obj.get_achievements_list()
