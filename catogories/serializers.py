from rest_framework import serializers
from .models import Form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
    def get_tech_stack_list(self, obj):
        """Returns tech stack as a list for the API"""
        return obj.get_tech_stack_list()
    
    def get_achievements_list(self, obj):
        """Returns achievements as a list for the API"""
        return obj.get_achievements_list()
