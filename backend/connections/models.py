import uuid
from django.conf import settings
from django.db import models
class FriendRequest(models.Model):
    class Status(models.TextChoices): PENDING='pending'; ACCEPTED='accepted'; REJECTED='rejected'; CANCELLED='cancelled'; REMOVED='removed'
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='sent_friend_requests')
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='received_friend_requests')
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: unique_together=[('sender','receiver')]; ordering=['-updated_at']
class Friend(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='friend_edges')
    friend=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='+')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=[('user','friend')]
