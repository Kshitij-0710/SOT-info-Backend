from rest_framework import viewsets, permissions
from .models import Form
from .serializers import FormSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all users,
    but require authentication for write operations.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD and OPTIONS requests without authentication
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class FormViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Forms:
    - Anonymous users can view forms (GET)
    - Authenticated users can create and manage their own forms
    """
    serializer_class = FormSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    
    def get_queryset(self):
        """
        Return filtered queryset based on authentication status:
        - For anonymous users or GET requests, return all forms
        - For authenticated users' write operations, return only their forms
        """
        base_queryset = Form.objects.select_related('user').order_by('-created_at')
        
        if self.action == 'list' or not self.request.user.is_authenticated:
            return base_queryset
        
        return base_queryset.filter(user=self.request.user)

    # Add this inside the FormViewSet class
    @action(detail=False, methods=['get'])
    def top_six(self, request):
        """Optimized endpoint just for homepage data"""
        # First filter for top_6 items only (much smaller dataset)
        top_forms = Form.objects.filter(is_top_6=True).select_related('user')
        
        # Pre-categorize on the server
        result = {
            'studentAchievements': self.get_serializer(
                top_forms.filter(user_type='STUDENT', category='achievement')[:6], 
                many=True
            ).data,
            'facultyAchievements': self.get_serializer(
                top_forms.filter(user_type='FACULTY', category='achievement')[:6], 
                many=True
            ).data,
            'studentProjects': self.get_serializer(
                top_forms.filter(user_type='STUDENT', category='project')[:6], 
                many=True
            ).data,
            'facultyProjects': self.get_serializer(
                top_forms.filter(user_type='FACULTY', category='project')[:6], 
                many=True
            ).data,
            'studentResearch': self.get_serializer(
                top_forms.filter(user_type='STUDENT', category='research')[:6], 
                many=True
            ).data,
            'facultyResearch': self.get_serializer(
                top_forms.filter(user_type='FACULTY', category='research')[:6], 
                many=True
            ).data,
        }
        
        return Response(result)
    
    def perform_create(self, serializer):
        """
        Save the form with the authenticated user and their user_type
        """
        if self.request.user.is_authenticated:
            serializer.save(
                user=self.request.user,
                user_type=self.request.user.user_type
            )
        else:
            # This should never happen since permission checks would prevent it
            raise PermissionError("Authentication required to create forms")