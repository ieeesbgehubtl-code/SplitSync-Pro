import uuid
from django.conf import settings
from django.db import models
class Trip(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=140); description=models.TextField(blank=True)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owned_trips')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
class TripMember(models.Model):
    class Role(models.TextChoices): OWNER='owner'; ADMIN='admin'; MEMBER='member'
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='memberships')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='trip_memberships')
    role=models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    joined_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=[('trip','user')]
class TripInvitation(models.Model):
    class Status(models.TextChoices): PENDING='pending'; ACCEPTED='accepted'; REJECTED='rejected'; CANCELLED='cancelled'
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='invitations')
    invited_user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='trip_invitations')
    invited_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='+')
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: unique_together=[('trip','invited_user')]
