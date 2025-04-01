from rest_framework import viewsets, permissions
from .models import Form
from .serializers import FormSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Placement
from .serializers import PlacementSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ReadOnlyOrAuthenticated(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all users,
    but require authentication for write operations.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD and OPTIONS requests without authentication
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write operations, require authentication
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD and OPTIONS requests without authentication
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only allowed to the owner
        return request.user and request.user.is_authenticated and obj.user.id == request.user.id

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
        - For authenticated users' write operations, return all forms
          (object-level permissions will be checked separately)
        """
        return Form.objects.select_related('user').order_by('-created_at')
    @action(detail=False, methods=['get'])
    def my_forms(self, request):
        """Endpoint to get only the current user's forms"""
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=401)
            
        forms = Form.objects.filter(user=request.user).select_related('user').order_by('-created_at')
        serializer = self.get_serializer(forms, many=True)
        return Response(serializer.data)

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
    @action(detail=False, methods=['get'])
    def top_six_ongoing(self, request):
        """Optimized endpoint for ongoing projects"""
        # First filter for top ongoing items only (much smaller dataset)
        ongoing_forms = Form.objects.filter(is_top_6=True, is_ongoing=True).select_related('user')
        
        # Pre-categorize on the server
        result = {
            'studentAchievements': self.get_serializer(
                ongoing_forms.filter(user_type='STUDENT', category='achievement')[:6], 
                many=True
            ).data,
            'facultyAchievements': self.get_serializer(
                ongoing_forms.filter(user_type='FACULTY', category='achievement')[:6], 
                many=True
            ).data,
            'studentProjects': self.get_serializer(
                ongoing_forms.filter(user_type='STUDENT', category='project')[:6], 
                many=True
            ).data,
            'facultyProjects': self.get_serializer(
                ongoing_forms.filter(user_type='FACULTY', category='project')[:6], 
                many=True
            ).data,
            'studentResearch': self.get_serializer(
                ongoing_forms.filter(user_type='STUDENT', category='research')[:6], 
                many=True
            ).data,
            'facultyResearch': self.get_serializer(
                ongoing_forms.filter(user_type='FACULTY', category='research')[:6], 
                many=True
            ).data,
        }
        
        return Response(result)
    def perform_create(self, serializer):
        """
        Save the form with the authenticated user and their user_type
        """
        serializer.save(
            user=self.request.user,
            user_type=self.request.user.user_type
        )


class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.all()
    serializer_class = PlacementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['company', 'date', 'student']
    search_fields = ['title', 'description', 'company', 'student']
    ordering_fields = ['date', 'package', 'company']
    ordering = ['-date']  # Default ordering by date (newest first)
    
    @action(detail=False, methods=['get'])
    def top_placements(self, request):
        """
        Retrieves the top 2 placements marked with top_2=True
        Returns them ordered by package value (highest first)
        """
        top_placements = self.get_queryset().filter(top_2=True).order_by('-package')[:2]
        serializer = self.get_serializer(top_placements, many=True)
        return Response(serializer.data)