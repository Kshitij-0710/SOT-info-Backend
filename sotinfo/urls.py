from django.contrib import admin
from django.urls import include, path
from .routing import router
from .docs import schema_view  
from django.views.generic import TemplateView
from linkedin_embed.views import LinkedInEmbedsAPI

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/linkedin-embeds/', LinkedInEmbedsAPI.as_view(), name='linkedin-embeds'),
]
