from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from activity.models import ActivityLog
from common.money import (
    split_equal,
    split_exact,
    split_percentage,
    split_shares,
    q,
    simplify_balances,
)
from notifications.models import Notification
from trips.models import TripMember
from trips.services import ensure_member
from .models import Expense, ExpenseParticipant


def _allocations(total, method, participant_data):
    ids = [str(p["user"].id) for p in participant_data]
    if method == Expense.SplitMethod.EQUAL:
        return split_equal(total, ids)
    if method in [Expense.SplitMethod.EXACT, Expense.SplitMethod.CUSTOM]:
        return split_exact(
            total, {str(p["user"].id): p["amount_owed"] for p in participant_data}
        )
    if method == Expense.SplitMethod.PERCENTAGE:
        return split_percentage(
            total, {str(p["user"].id): p["share_percentage"] for p in participant_data}
        )
    if method == Expense.SplitMethod.SHARES:
        return split_shares(
            total, {str(p["user"].id): p["share_units"] for p in participant_data}
        )
    raise serializers.ValidationError("Unsupported split method.")


@transaction.atomic
def create_expense(*, trip, actor, validated_data, participants):
    ensure_member(trip, actor)
    if not TripMember.objects.filter(
        trip=trip, user=validated_data["paid_by"], is_active=True
    ).exists():
        raise serializers.ValidationError("Payer must be an active trip member.")
    for p in participants:
        if not TripMember.objects.filter(
            trip=trip, user=p["user"], is_active=True
        ).exists():
            raise serializers.ValidationError(
                "All participants must be active trip members."
            )
    allocations = _allocations(
        validated_data["amount"], validated_data["split_method"], participants
    )
    expense = Expense.objects.create(
        trip=trip, created_by=actor, updated_by=actor, **validated_data
    )
    for p in participants:
        uid = str(p["user"].id)
        paid = (
            q(validated_data["amount"])
            if p["user"] == validated_data["paid_by"]
            else Decimal("0.00")
        )
        owed = allocations[uid]
        ExpenseParticipant.objects.create(
            expense=expense,
            user=p["user"],
            amount_owed=owed,
            amount_paid=paid,
            balance=q(paid - owed),
            split_type=validated_data["split_method"],
            share_percentage=p.get("share_percentage"),
            share_units=p.get("share_units"),
        )
        if p["user"] != actor:
            Notification.objects.create(
                user=p["user"],
                actor=actor,
                type=Notification.Type.EXPENSE_ADDED,
                title="Expense added",
                message=f"{actor.full_name} added {expense.title} in {trip.name}.",
                data={"expense_id": str(expense.id), "trip_id": str(trip.id)},
            )
    ActivityLog.objects.create(
        actor=actor,
        verb="expense_added",
        metadata={"trip_id": str(trip.id), "expense_id": str(expense.id)},
    )
    return expense


def trip_balances(trip):
    balances = {
        str(m.user_id): Decimal("0.00")
        for m in TripMember.objects.filter(trip=trip, is_active=True)
    }
    for p in ExpenseParticipant.objects.filter(
        expense__trip=trip, expense__is_deleted=False
    ):
        balances[str(p.user_id)] = q(
            balances.get(str(p.user_id), Decimal("0.00")) + p.balance
        )
    return balances


def trip_settlements(trip):
    return simplify_balances(trip_balances(trip))
