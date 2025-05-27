from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        '''
        will add parent_email field if parent unique email too is required as input
        while submitting feedback
        '''
        model = Feedback
        fields = ['id', 'parent_name', 'keep_anonymous', 'parent_email', 'school', 'subject', 'message']
        read_only_fields = ['id']
        

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if not user.is_authenticated or user.user_type != 'PARENT':
            raise serializers.ValidationError("Only parents are allowed to submit feedback.")
        return data
