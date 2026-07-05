import uuid
from django.conf import settings
from django.db import models
class ActivityLog(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    verb=models.CharField(max_length=80)
    metadata=models.JSONField(default=dict, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
