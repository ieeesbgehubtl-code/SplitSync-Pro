from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from .models import Trip, TripMember, TripInvitation
class TripSerializer(serializers.ModelSerializer):
    class Meta: model=Trip; fields=['id','name','description','owner','created_at','updated_at']; read_only_fields=['id','owner','created_at','updated_at']
class TripMemberSerializer(serializers.ModelSerializer):
    user=UserPublicSerializer(read_only=True)
    class Meta: model=TripMember; fields=['id','trip','user','role','joined_at']
class TripInvitationSerializer(serializers.ModelSerializer):
    invited_user=UserPublicSerializer(read_only=True); invited_by=UserPublicSerializer(read_only=True)
    class Meta: model=TripInvitation; fields=['id','trip','invited_user','invited_by','status','created_at','updated_at']
class InviteFriendSerializer(serializers.Serializer): invited_user_id=serializers.UUIDField()
