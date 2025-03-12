from rest_framework.routers import DefaultRouter
from authentication.views import AuthViewSet
from catogories.views import FormViewSet


router = DefaultRouter() 

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'forms', FormViewSet, basename='forms')