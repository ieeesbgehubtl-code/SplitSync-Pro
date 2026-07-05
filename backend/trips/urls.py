from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, TripViewSet, TripInvitationViewSet

router = DefaultRouter()
router.register("currencies", CurrencyViewSet, basename="currencies")
router.register("invitations", TripInvitationViewSet, basename="trip-invitations")
router.register("", TripViewSet, basename="trips")
urlpatterns = router.urls
