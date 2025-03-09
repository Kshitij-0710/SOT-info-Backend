from rest_framework.routers import DefaultRouter

from authentication.views import AuthViewSet
from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet, ProjectViewSet, ResearchViewSet


router = DefaultRouter() 

router.register(r'auth', AuthViewSet, basename='auth')

router.register(r'achievements', AchievementViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'research', ResearchViewSet)