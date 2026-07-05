from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserPublicSerializer
from trips.models import Trip
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payer = UserPublicSerializer(read_only=True)
    receiver = UserPublicSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "trip",
            "payer",
            "receiver",
            "amount",
            "method",
            "notes",
            "recorded_by",
            "paid_at",
        ]
        read_only_fields = ["id", "recorded_by", "paid_at"]


class PaymentCreateSerializer(serializers.Serializer):
    trip_id = serializers.UUIDField()
    payer_id = serializers.UUIDField()
    receiver_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    method = serializers.ChoiceField(choices=Payment.Method.choices)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Payment amount must be positive.")
        return value

    def create(self, vd):
        return Payment.objects.create(
            trip=Trip.objects.get(id=vd["trip_id"]),
            payer=User.objects.get(id=vd["payer_id"]),
            receiver=User.objects.get(id=vd["receiver_id"]),
            amount=vd["amount"],
            method=vd["method"],
            notes=vd.get("notes", ""),
            recorded_by=self.context["request"].user,
        )
