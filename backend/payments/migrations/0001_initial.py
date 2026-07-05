import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
 initial=True; dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL),('trips','0001_initial')]
 operations=[migrations.CreateModel(name='Payment',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('amount',models.DecimalField(decimal_places=2,max_digits=12)),('method',models.CharField(choices=[('cash','Cash'),('online','Online')],max_length=20)),('notes',models.TextField(blank=True)),('paid_at',models.DateTimeField(auto_now_add=True)),('payer',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='payments_made',to=settings.AUTH_USER_MODEL)),('receiver',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='payments_received',to=settings.AUTH_USER_MODEL)),('recorded_by',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='recorded_payments',to=settings.AUTH_USER_MODEL)),('trip',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='payments',to='trips.trip'))])]
