from rest_framework.routers import DefaultRouter

from authentication.views import AuthViewSet

router = DefaultRouter() 

router.register(r'auth', AuthViewSet, basename='auth')