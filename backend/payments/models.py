import uuid
from django.conf import settings
from django.db import models
from trips.models import Trip
class Payment(models.Model):
    class Method(models.TextChoices): CASH='cash'; ONLINE='online'
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='payments')
    payer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='payments_made')
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='payments_received')
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    method=models.CharField(max_length=20,choices=Method.choices)
    notes=models.TextField(blank=True)
    recorded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='recorded_payments')
    paid_at=models.DateTimeField(auto_now_add=True)
    class Meta: indexes=[models.Index(fields=['trip','paid_at']),models.Index(fields=['payer','receiver'])]
