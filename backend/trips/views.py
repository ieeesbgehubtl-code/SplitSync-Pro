from django.db import transaction
from rest_framework import viewsets, decorators, response, status, serializers
from accounts.models import User
from connections.services import are_friends
from notifications.models import Notification
from .models import Trip, TripMember, TripInvitation
from .serializers import TripSerializer, TripMemberSerializer, TripInvitationSerializer, InviteFriendSerializer
class TripViewSet(viewsets.ModelViewSet):
    serializer_class=TripSerializer; search_fields=['name','description']; ordering_fields=['created_at','updated_at','name']
    def get_queryset(self): return Trip.objects.filter(memberships__user=self.request.user).distinct()
    def perform_create(self,serializer):
        with transaction.atomic():
            trip=serializer.save(owner=self.request.user); TripMember.objects.create(trip=trip,user=self.request.user,role=TripMember.Role.OWNER)
    def _can_invite(self, trip): return TripMember.objects.filter(trip=trip,user=self.request.user,role__in=[TripMember.Role.OWNER,TripMember.Role.ADMIN]).exists()
    @decorators.action(detail=True, methods=['post'])
    def invite(self,request,pk=None):
        trip=self.get_object();
        if not self._can_invite(trip): raise serializers.ValidationError('Only trip owners and admins can invite members.')
        ser=InviteFriendSerializer(data=request.data); ser.is_valid(raise_exception=True); user=User.objects.get(id=ser.validated_data['invited_user_id'])
        if not are_friends(request.user,user): raise serializers.ValidationError('Only friends can be invited.')
        if TripMember.objects.filter(trip=trip,user=user).exists(): raise serializers.ValidationError('User is already in the trip.')
        inv,created=TripInvitation.objects.get_or_create(trip=trip,invited_user=user,defaults={'invited_by':request.user})
        if not created and inv.status==TripInvitation.Status.PENDING: raise serializers.ValidationError('A pending invitation already exists.')
        inv.status=TripInvitation.Status.PENDING; inv.invited_by=request.user; inv.save()
        Notification.objects.create(user=user,actor=request.user,type=Notification.Type.TRIP_INVITATION_RECEIVED,title='Trip invitation',message=f'You were invited to {trip.name}.',data={'trip_id':str(trip.id),'invitation_id':str(inv.id)})
        return response.Response({'success':True,'data':TripInvitationSerializer(inv).data},status=status.HTTP_201_CREATED)
    @decorators.action(detail=True, methods=['get'])
    def members(self,request,pk=None): return response.Response({'success':True,'data':TripMemberSerializer(self.get_object().memberships.select_related('user'),many=True).data})
    @decorators.action(detail=True, methods=['get'])
    def pending_invitations(self,request,pk=None): return response.Response({'success':True,'data':TripInvitationSerializer(self.get_object().invitations.filter(status='pending'),many=True).data})
class TripInvitationViewSet(viewsets.GenericViewSet):
    serializer_class=TripInvitationSerializer
    def get_queryset(self): return TripInvitation.objects.filter(invited_user=self.request.user)
    @decorators.action(detail=True, methods=['post'])
    @transaction.atomic
    def accept(self,request,pk=None):
        inv=self.get_object(); inv.status=TripInvitation.Status.ACCEPTED; inv.save(update_fields=['status','updated_at']); TripMember.objects.get_or_create(trip=inv.trip,user=request.user)
        Notification.objects.create(user=inv.invited_by,actor=request.user,type=Notification.Type.TRIP_INVITATION_ACCEPTED,title='Trip invitation accepted',message=f'{request.user.full_name} joined {inv.trip.name}.')
        return response.Response({'success':True,'data':TripInvitationSerializer(inv).data})
    @decorators.action(detail=True, methods=['post'])
    def reject(self,request,pk=None):
        inv=self.get_object(); inv.status=TripInvitation.Status.REJECTED; inv.save(update_fields=['status','updated_at']); Notification.objects.create(user=inv.invited_by,actor=request.user,type=Notification.Type.TRIP_INVITATION_REJECTED,title='Trip invitation rejected',message=f'{request.user.full_name} declined {inv.trip.name}.'); return response.Response({'success':True,'data':TripInvitationSerializer(inv).data})
    @decorators.action(detail=True, methods=['post'])
    def cancel(self,request,pk=None):
        inv=TripInvitation.objects.get(pk=pk)
        if inv.invited_by != request.user: raise serializers.ValidationError('Only inviter can cancel.')
        inv.status=TripInvitation.Status.CANCELLED; inv.save(update_fields=['status','updated_at']); return response.Response({'success':True,'data':TripInvitationSerializer(inv).data})
