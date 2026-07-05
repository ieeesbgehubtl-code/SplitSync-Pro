from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from common.validators import require_cloudinary_url
from .models import Currency, Trip, TripMember, TripInvitation
class CurrencySerializer(serializers.ModelSerializer):
    class Meta: model=Currency; fields=['code','name','symbol','decimal_places','is_active']
class TripSerializer(serializers.ModelSerializer):
    member_count=serializers.IntegerField(read_only=True, default=0)
    def validate_trip_image(self,value): return require_cloudinary_url(value)
    def validate(self,attrs):
        if attrs.get('start_date') and attrs.get('end_date') and attrs['end_date'] < attrs['start_date']: raise serializers.ValidationError('End date cannot be before start date.')
        return attrs
    class Meta: model=Trip; fields=['id','name','destination','description','trip_image','currency','start_date','end_date','status','owner','member_count','created_at','updated_at']; read_only_fields=['id','owner','created_at','updated_at','member_count']
class TripMemberSerializer(serializers.ModelSerializer):
    user=UserPublicSerializer(read_only=True)
    class Meta: model=TripMember; fields=['id','trip','user','role','is_active','joined_at']
class TripInvitationSerializer(serializers.ModelSerializer):
    invited_user=UserPublicSerializer(read_only=True); invited_by=UserPublicSerializer(read_only=True)
    class Meta: model=TripInvitation; fields=['id','trip','invited_user','invited_by','status','created_at','updated_at']
class InviteFriendSerializer(serializers.Serializer): invited_user_id=serializers.UUIDField()
class TransferOwnershipSerializer(serializers.Serializer): user_id=serializers.UUIDField()
