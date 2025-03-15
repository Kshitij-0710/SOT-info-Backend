from rest_framework import viewsets, permissions
from .models import Form
from .serializers import FormSerializer

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