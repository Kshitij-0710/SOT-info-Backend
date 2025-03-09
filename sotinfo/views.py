from rest_framework import viewsets
from .models import Achievement, Project, Research
from .serializers import AchievementSerializer, ProjectSerializer, ResearchSerializer

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all().order_by('-created_at')
    serializer_class = AchievementSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer

class ResearchViewSet(viewsets.ModelViewSet):
    queryset = Research.objects.all().order_by('-created_at')
    serializer_class = ResearchSerializer
