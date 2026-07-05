from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from accounts.models import User
from .models import FriendRequest, Friend

class FriendRequestSerializer(serializers.ModelSerializer):
    sender=UserPublicSerializer(read_only=True); receiver=UserPublicSerializer(read_only=True)
    class Meta: model=FriendRequest; fields=['id','sender','receiver','status','created_at','updated_at']
class SendFriendRequestSerializer(serializers.Serializer):
    receiver_id=serializers.UUIDField()
    def validate_receiver_id(self,value):
        if not User.objects.filter(id=value).exists(): raise serializers.ValidationError('User not found.')
        return value
class FriendSerializer(serializers.ModelSerializer):
    friend=UserPublicSerializer(read_only=True); mutual_trips=serializers.IntegerField(read_only=True, default=0); total_shared_expenses=serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True, default=0)
    class Meta: model=Friend; fields=['id','friend','created_at','mutual_trips','total_shared_expenses']
