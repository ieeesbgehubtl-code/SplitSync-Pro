from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from rest_framework import views, response
from expenses.models import Expense
from trips.models import Trip


class DashboardView(views.APIView):
    def get(self, request):
        trips = Trip.objects.filter(
            memberships__user=request.user,
            memberships__is_active=True,
            is_deleted=False,
        )
        expenses = Expense.objects.filter(trip__in=trips, is_deleted=False)
        monthly = list(
            expenses.annotate(month=TruncMonth("expense_date"))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )
        categories = list(
            expenses.values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")[:10]
        )
        data = {
            "trip_count": trips.count(),
            "friends_count": request.user.friend_edges.count(),
            "recent_trips": list(
                trips.values("id", "name", "destination", "status", "start_date")[:5]
            ),
            "recent_expenses": list(
                expenses.values("id", "title", "amount", "expense_date", "trip__name")[
                    :10
                ]
            ),
            "monthly_expense_chart": monthly,
            "category_pie_chart": categories,
            "expense_count": expenses.count(),
        }
        return response.Response({"success": True, "data": data})
