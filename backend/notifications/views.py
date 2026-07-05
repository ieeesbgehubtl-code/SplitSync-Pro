from django.utils import timezone
from rest_framework import viewsets, decorators, response, status
from .models import Notification
from .serializers import NotificationSerializer
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class=NotificationSerializer; search_fields=['title','message']; ordering_fields=['created_at','read_at']
    def get_queryset(self): return Notification.objects.filter(user=self.request.user)
    @decorators.action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        n=self.get_object(); n.read_at=timezone.now(); n.save(update_fields=['read_at']); return response.Response({'success':True,'data':self.get_serializer(n).data})
    @decorators.action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        count=self.get_queryset().filter(read_at__isnull=True).update(read_at=timezone.now()); return response.Response({'success':True,'data':{'updated':count}})
    def destroy(self,request,*args,**kwargs): super().destroy(request,*args,**kwargs); return response.Response({'success':True}, status=status.HTTP_204_NO_CONTENT)
