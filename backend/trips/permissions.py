from rest_framework.permissions import BasePermission
from .models import TripMember
class IsTripOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return TripMember.objects.filter(trip=obj, user=request.user, role__in=[TripMember.Role.OWNER, TripMember.Role.ADMIN], is_active=True).exists()
