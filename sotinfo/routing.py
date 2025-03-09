from rest_framework.routers import DefaultRouter

from authentication.views import AuthViewSet
from rest_framework.routers import DefaultRouter
from catogories.views import AchievementViewSet, ProjectViewSet, ResearchViewSet


router = DefaultRouter() 

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'achievements', AchievementViewSet, basename='ach')
router.register(r'projects', ProjectViewSet,basename='projects')
router.register(r'research', ResearchViewSet,basename='res')