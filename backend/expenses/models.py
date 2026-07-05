import uuid
from django.conf import settings
from django.db import models
from trips.models import Trip
class Category(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=80)
    icon=models.CharField(max_length=40, blank=True)
    color=models.CharField(max_length=20, blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    is_system=models.BooleanField(default=False)
    class Meta: unique_together=[('name','created_by')]; ordering=['name']
class Expense(models.Model):
    class SplitMethod(models.TextChoices): EQUAL='equal'; EXACT='exact'; PERCENTAGE='percentage'; SHARES='shares'; CUSTOM='custom'
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name='expenses')
    title=models.CharField(max_length=160, db_index=True); description=models.TextField(blank=True)
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    paid_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='paid_expenses')
    expense_date=models.DateField(db_index=True)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='expenses')
    receipt_image=models.URLField(blank=True)
    split_method=models.CharField(max_length=20,choices=SplitMethod.choices)
    notes=models.TextField(blank=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='created_expenses')
    updated_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='updated_expenses')
    is_deleted=models.BooleanField(default=False, db_index=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: indexes=[models.Index(fields=['trip','expense_date']), models.Index(fields=['paid_by','expense_date'])]
class ExpenseParticipant(models.Model):
    class SettlementStatus(models.TextChoices): OPEN='open'; PARTIAL='partial'; SETTLED='settled'
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense=models.ForeignKey(Expense,on_delete=models.CASCADE,related_name='participants')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='expense_participants')
    amount_owed=models.DecimalField(max_digits=12,decimal_places=2)
    amount_paid=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    balance=models.DecimalField(max_digits=12,decimal_places=2)
    split_type=models.CharField(max_length=20)
    share_percentage=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    share_units=models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True)
    settlement_status=models.CharField(max_length=20,choices=SettlementStatus.choices,default=SettlementStatus.OPEN)
    class Meta: unique_together=[('expense','user')]; indexes=[models.Index(fields=['user','settlement_status'])]
class ExpenseComment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense=models.ForeignKey(Expense,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    body=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
class ExpenseAudit(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense=models.ForeignKey(Expense,on_delete=models.CASCADE,related_name='audit_entries')
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    action=models.CharField(max_length=40); before=models.JSONField(default=dict,blank=True); after=models.JSONField(default=dict,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
