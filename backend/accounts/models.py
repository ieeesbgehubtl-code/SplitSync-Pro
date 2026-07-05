import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=160)
    profile_picture = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    last_active = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, unique=True)
    REQUIRED_FIELDS = ['email','full_name']
    def save(self,*args,**kwargs):
        if self.pk and User.objects.filter(pk=self.pk).exists():
            old=User.objects.only('username').get(pk=self.pk)
            if old.username != self.username and not getattr(self, '_admin_username_change', False):
                raise ValueError('Username cannot be changed after registration.')
        super().save(*args,**kwargs)
