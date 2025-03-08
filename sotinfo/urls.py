from django.contrib import admin
from django.urls import include, path
from .routing import router
from .docs import schema_view  
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet, ProjectViewSet, ResearchViewSet

# Registering new viewsets
router.register(r'achievements', AchievementViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'research', ResearchViewSet)

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
