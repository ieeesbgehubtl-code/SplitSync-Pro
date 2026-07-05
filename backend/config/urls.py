from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/friends/", include("connections.urls")),
    path("api/trips/", include("trips.urls")),
    path("api/expenses/", include("expenses.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/notifications/", include("notifications.urls")),
]
