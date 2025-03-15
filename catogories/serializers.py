from rest_framework import serializers
from .models import Form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = fields = [
            'id', 'title', 'description', 'team_members', 
            'tech_stack', 'tech_stack', 'projecturl', 
            'achivements', 'achivements', 'from_date', 
            'to_date', 'category', 'is_top_6','created_at', 'user_type'
        ]
        read_only_fields = ['user_type', 'is_top_6']
    def get_tech_stack_list(self, obj):
        """Returns tech stack as a list for the API"""
        return obj.get_tech_stack_list()
    
    def get_achievements_list(self, obj):
        """Returns achievements as a list for the API"""
        return obj.get_achievements_list()
