from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Form
from .serializers import FormSerializer

class FormViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Forms
    """
    queryset = Form.objects.all().order_by('-created_at')
    serializer_class = FormSerializer
    def get_queryset(self):
        """Return forms created by the authenticated user"""
        return Form.objects.filter(user=self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Save the form with the authenticated user and their user_type"""
        serializer.save(
            user=self.request.user,
            user_type=self.request.user.user_type
        )