from rest_framework import viewsets, decorators, response, status, mixins
from trips.models import Trip
from .models import Category, Expense, ExpenseComment
from .serializers import CategorySerializer, ExpenseSerializer, ExpenseCreateSerializer, ExpenseCommentSerializer
from .services import trip_balances, trip_settlements
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class=CategorySerializer; search_fields=['name']; ordering_fields=['name']
    def get_queryset(self): return Category.objects.filter(created_by__isnull=True) | Category.objects.filter(created_by=self.request.user)
    def perform_create(self,serializer): serializer.save(created_by=self.request.user)
class ExpenseViewSet(viewsets.ModelViewSet):
    search_fields=['title','description','notes']; filterset_fields=['trip','category','paid_by','split_method','expense_date']; ordering_fields=['expense_date','amount','created_at']
    def get_queryset(self): return Expense.objects.filter(trip__memberships__user=self.request.user,trip__memberships__is_active=True,is_deleted=False).select_related('trip','paid_by','category').prefetch_related('participants')
    def get_serializer_class(self): return ExpenseCreateSerializer if self.action=='create' else ExpenseSerializer
    def create(self,request,*args,**kwargs): ser=self.get_serializer(data=request.data); ser.is_valid(raise_exception=True); expense=ser.save(); return response.Response({'success':True,'data':ExpenseSerializer(expense).data},status=status.HTTP_201_CREATED)
    def destroy(self,request,*args,**kwargs): expense=self.get_object(); expense.is_deleted=True; expense.updated_by=request.user; expense.save(update_fields=['is_deleted','updated_by','updated_at']); return response.Response({'success':True},status=status.HTTP_204_NO_CONTENT)
    @decorators.action(detail=True,methods=['post'])
    def comments(self,request,pk=None): comment=ExpenseComment.objects.create(expense=self.get_object(),user=request.user,body=request.data.get('body','')); return response.Response({'success':True,'data':ExpenseCommentSerializer(comment).data},status=status.HTTP_201_CREATED)
class TripSettlementViewSet(viewsets.GenericViewSet):
    @decorators.action(detail=True,methods=['get'])
    def balances(self,request,pk=None): trip=Trip.objects.get(id=pk,memberships__user=request.user); return response.Response({'success':True,'data':trip_balances(trip)})
    @decorators.action(detail=True,methods=['get'])
    def simplify(self,request,pk=None): trip=Trip.objects.get(id=pk,memberships__user=request.user); return response.Response({'success':True,'data':trip_settlements(trip)})
