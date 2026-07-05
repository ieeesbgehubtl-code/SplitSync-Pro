import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("friend_request_received", "Friend Request Received"),
                            ("friend_request_accepted", "Friend Request Accepted"),
                            ("trip_invitation_received", "Trip Invitation Received"),
                            ("trip_invitation_accepted", "Trip Invitation Accepted"),
                            ("trip_invitation_rejected", "Trip Invitation Rejected"),
                            ("removed_from_trip", "Removed From Trip"),
                            ("added_to_trip", "Added To Trip"),
                            ("expense_added", "Expense Added"),
                            ("settlement_completed", "Settlement Completed"),
                            ("trip_closed", "Trip Closed"),
                        ],
                        max_length=40,
                    ),
                ),
                ("title", models.CharField(max_length=160)),
                ("message", models.TextField()),
                ("data", models.JSONField(blank=True, default=dict)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "actor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        )
    ]
