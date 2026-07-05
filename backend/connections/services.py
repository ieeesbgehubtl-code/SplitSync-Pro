from django.db import transaction
from rest_framework import serializers
from notifications.models import Notification
from .models import FriendRequest, Friend


def are_friends(a, b):
    return Friend.objects.filter(user=a, friend=b).exists()


@transaction.atomic
def send_request(sender, receiver):
    if sender == receiver:
        raise serializers.ValidationError("Cannot add yourself as a friend.")
    if are_friends(sender, receiver):
        raise serializers.ValidationError("Users are already friends.")
    existing = (
        FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
        or FriendRequest.objects.filter(
            sender=receiver, receiver=sender, status=FriendRequest.Status.PENDING
        ).first()
    )
    if existing and existing.status == FriendRequest.Status.PENDING:
        raise serializers.ValidationError("A pending request already exists.")
    req, _ = FriendRequest.objects.update_or_create(
        sender=sender,
        receiver=receiver,
        defaults={"status": FriendRequest.Status.PENDING},
    )
    Notification.objects.create(
        user=receiver,
        actor=sender,
        type=Notification.Type.FRIEND_REQUEST_RECEIVED,
        title="New friend request",
        message=f"{sender.full_name} sent you a friend request.",
        data={"request_id": str(req.id)},
    )
    return req


@transaction.atomic
def accept_request(req, actor):
    if req.receiver != actor:
        raise serializers.ValidationError("Only the receiver can accept this request.")
    if req.status != FriendRequest.Status.PENDING:
        raise serializers.ValidationError("Request is not pending.")
    req.status = FriendRequest.Status.ACCEPTED
    req.save(update_fields=["status", "updated_at"])
    Friend.objects.get_or_create(user=req.sender, friend=req.receiver)
    Friend.objects.get_or_create(user=req.receiver, friend=req.sender)
    Notification.objects.create(
        user=req.sender,
        actor=req.receiver,
        type=Notification.Type.FRIEND_REQUEST_ACCEPTED,
        title="Friend request accepted",
        message=f"{req.receiver.full_name} accepted your request.",
        data={"request_id": str(req.id)},
    )
    return req
