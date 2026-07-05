from django.db import transaction
from django.db.models import Count
from rest_framework import viewsets, decorators, response, status, serializers, mixins
from accounts.models import User
from connections.services import are_friends
from notifications.models import Notification
from .models import Currency, Trip, TripMember, TripInvitation
from .serializers import (
    CurrencySerializer,
    TripSerializer,
    TripMemberSerializer,
    TripInvitationSerializer,
    InviteFriendSerializer,
    TransferOwnershipSerializer,
)
from .services import ensure_owner_or_admin, remove_member, transfer_ownership


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.filter(is_active=True)
    serializer_class = CurrencySerializer
    search_fields = ["code", "name"]
    ordering_fields = ["code", "name"]


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = TripSerializer
    search_fields = ["name", "description", "destination"]
    ordering_fields = ["created_at", "updated_at", "name", "start_date", "status"]
    filterset_fields = ["status", "currency"]

    def get_queryset(self):
        return (
            Trip.objects.filter(
                memberships__user=self.request.user,
                memberships__is_active=True,
                is_deleted=False,
            )
            .annotate(member_count=Count("memberships"))
            .distinct()
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            trip = serializer.save(owner=self.request.user)
            TripMember.objects.create(
                trip=trip, user=self.request.user, role=TripMember.Role.OWNER
            )

    def _can_invite(self, trip):
        return TripMember.objects.filter(
            trip=trip,
            user=self.request.user,
            role__in=[TripMember.Role.OWNER, TripMember.Role.ADMIN],
            is_active=True,
        ).exists()

    @decorators.action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        trip = self.get_object()
        if not self._can_invite(trip):
            raise serializers.ValidationError(
                "Only trip owners and admins can invite members."
            )
        ser = InviteFriendSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = User.objects.get(id=ser.validated_data["invited_user_id"])
        if not are_friends(request.user, user):
            raise serializers.ValidationError("Only friends can be invited.")
        if TripMember.objects.filter(trip=trip, user=user, is_active=True).exists():
            raise serializers.ValidationError("User is already in the trip.")
        inv, created = TripInvitation.objects.get_or_create(
            trip=trip, invited_user=user, defaults={"invited_by": request.user}
        )
        if not created and inv.status == TripInvitation.Status.PENDING:
            raise serializers.ValidationError("A pending invitation already exists.")
        inv.status = TripInvitation.Status.PENDING
        inv.invited_by = request.user
        inv.save()
        Notification.objects.create(
            user=user,
            actor=request.user,
            type=Notification.Type.TRIP_INVITATION_RECEIVED,
            title="Trip invitation",
            message=f"You were invited to {trip.name}.",
            data={"trip_id": str(trip.id), "invitation_id": str(inv.id)},
        )
        return response.Response(
            {"success": True, "data": TripInvitationSerializer(inv).data},
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(detail=True, methods=["get"])
    def members(self, request, pk=None):
        return response.Response(
            {
                "success": True,
                "data": TripMemberSerializer(
                    self.get_object()
                    .memberships.filter(is_active=True)
                    .select_related("user"),
                    many=True,
                ).data,
            }
        )

    @decorators.action(detail=True, methods=["get"])
    def pending_invitations(self, request, pk=None):
        return response.Response(
            {
                "success": True,
                "data": TripInvitationSerializer(
                    self.get_object().invitations.filter(status="pending"), many=True
                ).data,
            }
        )

    @decorators.action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        trip = self.get_object()
        ensure_owner_or_admin(trip, request.user)
        trip.status = Trip.Status.CLOSED
        trip.save(update_fields=["status", "updated_at"])
        return response.Response(
            {"success": True, "data": self.get_serializer(trip).data}
        )

    @decorators.action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        trip = self.get_object()
        ensure_owner_or_admin(trip, request.user)
        trip.status = Trip.Status.ARCHIVED
        trip.save(update_fields=["status", "updated_at"])
        return response.Response(
            {"success": True, "data": self.get_serializer(trip).data}
        )

    @decorators.action(detail=True, methods=["post"])
    def transfer_ownership(self, request, pk=None):
        trip = self.get_object()
        ser = TransferOwnershipSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        trip = transfer_ownership(
            trip, request.user, User.objects.get(id=ser.validated_data["user_id"])
        )
        return response.Response(
            {"success": True, "data": self.get_serializer(trip).data}
        )

    @decorators.action(
        detail=True, methods=["post"], url_path="members/(?P<member_id>[^/.]+)/remove"
    )
    def remove_member(self, request, pk=None, member_id=None):
        member = TripMember.objects.get(id=member_id, trip=self.get_object())
        remove_member(member.trip, request.user, member)
        return response.Response({"success": True})

    def destroy(self, request, *args, **kwargs):
        trip = self.get_object()
        ensure_owner_or_admin(trip, request.user)
        trip.is_deleted = True
        trip.save(update_fields=["is_deleted", "updated_at"])
        return response.Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


class TripInvitationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = TripInvitationSerializer
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        return TripInvitation.objects.filter(
            invited_user=self.request.user
        ).select_related("trip", "invited_user", "invited_by")

    @decorators.action(detail=True, methods=["post"])
    @transaction.atomic
    def accept(self, request, pk=None):
        inv = self.get_object()
        inv.status = TripInvitation.Status.ACCEPTED
        inv.save(update_fields=["status", "updated_at"])
        TripMember.objects.update_or_create(
            trip=inv.trip,
            user=request.user,
            defaults={"is_active": True, "role": TripMember.Role.MEMBER},
        )
        Notification.objects.create(
            user=inv.invited_by,
            actor=request.user,
            type=Notification.Type.TRIP_INVITATION_ACCEPTED,
            title="Trip invitation accepted",
            message=f"{request.user.full_name} joined {inv.trip.name}.",
        )
        Notification.objects.create(
            user=request.user,
            actor=inv.invited_by,
            type=Notification.Type.ADDED_TO_TRIP,
            title="Added to trip",
            message=f"You joined {inv.trip.name}.",
        )
        return response.Response(
            {"success": True, "data": TripInvitationSerializer(inv).data}
        )

    @decorators.action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        inv = self.get_object()
        inv.status = TripInvitation.Status.REJECTED
        inv.save(update_fields=["status", "updated_at"])
        Notification.objects.create(
            user=inv.invited_by,
            actor=request.user,
            type=Notification.Type.TRIP_INVITATION_REJECTED,
            title="Trip invitation rejected",
            message=f"{request.user.full_name} declined {inv.trip.name}.",
        )
        return response.Response(
            {"success": True, "data": TripInvitationSerializer(inv).data}
        )

    @decorators.action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        inv = TripInvitation.objects.get(pk=pk)
        if inv.invited_by != request.user:
            raise serializers.ValidationError("Only inviter can cancel.")
        inv.status = TripInvitation.Status.CANCELLED
        inv.save(update_fields=["status", "updated_at"])
        return response.Response(
            {"success": True, "data": TripInvitationSerializer(inv).data}
        )
