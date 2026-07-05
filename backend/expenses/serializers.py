from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserPublicSerializer
from common.validators import require_cloudinary_url
from trips.models import Trip
from .models import Category, Expense, ExpenseParticipant, ExpenseComment
from .services import create_expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "icon", "color", "is_system"]


class ExpenseParticipantInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    amount_owed = serializers.DecimalField(
        max_digits=12, decimal_places=2, required=False
    )
    share_percentage = serializers.DecimalField(
        max_digits=6, decimal_places=2, required=False
    )
    share_units = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=False
    )


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ExpenseParticipant
        fields = [
            "id",
            "user",
            "amount_owed",
            "amount_paid",
            "balance",
            "split_type",
            "share_percentage",
            "share_units",
            "settlement_status",
        ]


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True, read_only=True)
    paid_by = UserPublicSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "trip",
            "title",
            "description",
            "amount",
            "paid_by",
            "expense_date",
            "category",
            "receipt_image",
            "split_method",
            "participants",
            "notes",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class ExpenseCreateSerializer(serializers.Serializer):
    trip_id = serializers.UUIDField()
    title = serializers.CharField(max_length=160)
    description = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    paid_by_id = serializers.UUIDField()
    expense_date = serializers.DateField()
    category_id = serializers.UUIDField()
    receipt_image = serializers.URLField(required=False, allow_blank=True)
    split_method = serializers.ChoiceField(choices=Expense.SplitMethod.choices)
    notes = serializers.CharField(required=False, allow_blank=True)
    participants = ExpenseParticipantInputSerializer(many=True)

    def validate_receipt_image(self, value):
        return require_cloudinary_url(value)

    def create(self, validated_data):
        parts = validated_data.pop("participants")
        trip = Trip.objects.get(id=validated_data.pop("trip_id"))
        paid_by = User.objects.get(id=validated_data.pop("paid_by_id"))
        category = Category.objects.get(id=validated_data.pop("category_id"))
        participants = [
            {**p, "user": User.objects.get(id=p.pop("user_id"))} for p in parts
        ]
        return create_expense(
            trip=trip,
            actor=self.context["request"].user,
            validated_data={**validated_data, "paid_by": paid_by, "category": category},
            participants=participants,
        )


class ExpenseCommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = ExpenseComment
        fields = ["id", "expense", "user", "body", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
