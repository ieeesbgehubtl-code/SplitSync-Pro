from django.db import transaction
from rest_framework import viewsets, response, status
from notifications.models import Notification
from trips.models import TripMember
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    filterset_fields = ["trip", "payer", "receiver", "method"]
    ordering_fields = ["paid_at", "amount"]

    def get_queryset(self):
        return Payment.objects.filter(
            trip__memberships__user=self.request.user, trip__memberships__is_active=True
        ).select_related("trip", "payer", "receiver")

    def get_serializer_class(self):
        return PaymentCreateSerializer if self.action == "create" else PaymentSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        pay = ser.save()
        for user in [pay.payer, pay.receiver]:
            Notification.objects.create(
                user=user,
                actor=request.user,
                type=Notification.Type.SETTLEMENT_COMPLETED,
                title="Settlement recorded",
                message=f"{pay.payer.full_name} paid {pay.receiver.full_name} {pay.amount}.",
                data={"payment_id": str(pay.id), "trip_id": str(pay.trip_id)},
            )
        return response.Response(
            {"success": True, "data": PaymentSerializer(pay).data},
            status=status.HTTP_201_CREATED,
        )
