from rest_framework.routers import DefaultRouter
from .views import TripViewSet, TripInvitationViewSet
router=DefaultRouter(); router.register('invitations',TripInvitationViewSet,basename='trip-invitations'); router.register('',TripViewSet,basename='trips')
urlpatterns=router.urls
