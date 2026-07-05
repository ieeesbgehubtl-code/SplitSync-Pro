from django.db import transaction
from django.db.models import Case, When, Value, IntegerField, Q
from rest_framework import viewsets, mixins, decorators, response, status, serializers
from accounts.models import User
from accounts.serializers import UserPublicSerializer
from .models import FriendRequest, Friend
from .serializers import (
    FriendRequestSerializer,
    SendFriendRequestSerializer,
    FriendSerializer,
)
from .services import send_request, accept_request


class UserSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserPublicSerializer
    search_fields = ["username", "full_name", "email"]
    ordering_fields = ["username", "full_name", "created_at"]

    def get_queryset(self):
        q = self.request.query_params.get("search") or self.request.query_params.get(
            "q", ""
        )
        qs = User.objects.exclude(id=self.request.user.id)
        if q:
            qs = qs.filter(
                Q(username__icontains=q)
                | Q(full_name__icontains=q)
                | Q(email__iexact=q)
            )
        return qs.annotate(
            rank=Case(
                When(username__istartswith=q, then=Value(0)),
                When(username__icontains=q, then=Value(1)),
                When(full_name__icontains=q, then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by("rank", "username")


class FriendRequestViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = FriendRequestSerializer
    ordering_fields = ["created_at", "updated_at", "status"]
    filterset_fields = ["status"]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).select_related("sender", "receiver")

    @decorators.action(detail=False, methods=["post"])
    def send(self, request):
        ser = SendFriendRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        req = send_request(
            request.user, User.objects.get(id=ser.validated_data["receiver_id"])
        )
        return response.Response(
            {"success": True, "data": FriendRequestSerializer(req).data},
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        return response.Response(
            {
                "success": True,
                "data": FriendRequestSerializer(
                    accept_request(self.get_object(), request.user)
                ).data,
            }
        )

    @decorators.action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        req = self.get_object()
        if req.receiver != request.user:
            raise serializers.ValidationError("Only receiver can reject.")
        req.status = FriendRequest.Status.REJECTED
        req.save(update_fields=["status", "updated_at"])
        return response.Response(
            {"success": True, "data": FriendRequestSerializer(req).data}
        )

    @decorators.action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        req = self.get_object()
        if req.sender != request.user:
            raise serializers.ValidationError("Only sender can cancel.")
        req.status = FriendRequest.Status.CANCELLED
        req.save(update_fields=["status", "updated_at"])
        return response.Response(
            {"success": True, "data": FriendRequestSerializer(req).data}
        )


class FriendViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = FriendSerializer
    search_fields = ["friend__username", "friend__full_name"]
    ordering_fields = ["created_at", "friend__last_active"]

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user).select_related("friend")

    @decorators.action(detail=True, methods=["delete"])
    @transaction.atomic
    def remove(self, request, pk=None):
        edge = self.get_object()
        Friend.objects.filter(user=edge.friend, friend=request.user).delete()
        edge.delete()
        return response.Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
