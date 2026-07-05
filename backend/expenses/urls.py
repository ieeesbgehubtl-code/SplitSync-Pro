from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ExpenseViewSet, TripSettlementViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("trip-settlements", TripSettlementViewSet, basename="trip-settlements")
router.register("", ExpenseViewSet, basename="expenses")
urlpatterns = router.urls
