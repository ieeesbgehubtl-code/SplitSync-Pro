import uuid
from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Type(models.TextChoices):
        FRIEND_REQUEST_RECEIVED = "friend_request_received"
        FRIEND_REQUEST_ACCEPTED = "friend_request_accepted"
        TRIP_INVITATION_RECEIVED = "trip_invitation_received"
        TRIP_INVITATION_ACCEPTED = "trip_invitation_accepted"
        TRIP_INVITATION_REJECTED = "trip_invitation_rejected"
        REMOVED_FROM_TRIP = "removed_from_trip"
        ADDED_TO_TRIP = "added_to_trip"
        EXPENSE_ADDED = "expense_added"
        SETTLEMENT_COMPLETED = "settlement_completed"
        TRIP_CLOSED = "trip_closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    type = models.CharField(max_length=40, choices=Type.choices)
    title = models.CharField(max_length=160)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
