from django.db import transaction
from rest_framework import serializers
from notifications.models import Notification
from .models import Trip, TripMember

def ensure_member(trip, user):
    if not TripMember.objects.filter(trip=trip,user=user,is_active=True).exists(): raise serializers.ValidationError('Only trip members can perform this action.')

def ensure_owner_or_admin(trip, user):
    if not TripMember.objects.filter(trip=trip,user=user,role__in=[TripMember.Role.OWNER,TripMember.Role.ADMIN],is_active=True).exists(): raise serializers.ValidationError('Only trip owners and admins can perform this action.')

@transaction.atomic
def remove_member(trip, actor, member):
    ensure_owner_or_admin(trip, actor)
    if member.user == trip.owner: raise serializers.ValidationError('Transfer ownership before removing the owner.')
    member.is_active=False; member.save(update_fields=['is_active'])
    Notification.objects.create(user=member.user, actor=actor, type=Notification.Type.REMOVED_FROM_TRIP, title='Removed from trip', message=f'You were removed from {trip.name}.')
    return member

@transaction.atomic
def transfer_ownership(trip, actor, new_owner):
    if trip.owner != actor: raise serializers.ValidationError('Only the owner can transfer ownership.')
    membership=TripMember.objects.get(trip=trip,user=new_owner,is_active=True)
    TripMember.objects.filter(trip=trip,user=actor).update(role=TripMember.Role.ADMIN)
    membership.role=TripMember.Role.OWNER; membership.save(update_fields=['role'])
    trip.owner=new_owner; trip.save(update_fields=['owner','updated_at'])
    return trip
