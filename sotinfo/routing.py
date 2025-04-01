from rest_framework.routers import DefaultRouter
from authentication.views import AuthViewSet
from catogories.views import EventRegistrationViewSet, FormViewSet,PlacementViewSet, EventViewSet


router = DefaultRouter() 

router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'forms', FormViewSet, basename='forms')
router.register(r'placements',PlacementViewSet,basename='placement')
router.register(r'events', EventViewSet, basename='events')
router.register(r'event-registrations', EventRegistrationViewSet, basename='event-registrations')
