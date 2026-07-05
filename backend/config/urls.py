from django.contrib import admin
from django.urls import path, include
urlpatterns=[path('admin/', admin.site.urls), path('api/auth/', include('accounts.urls')), path('api/friends/', include('connections.urls')), path('api/trips/', include('trips.urls')), path('api/notifications/', include('notifications.urls'))]
