import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_currencies(apps, schema_editor):
    Currency = apps.get_model("trips", "Currency")
    Currency.objects.bulk_create(
        [
            Currency(code="INR", name="Indian Rupee", symbol="₹"),
            Currency(code="USD", name="US Dollar", symbol="$"),
            Currency(code="EUR", name="Euro", symbol="€"),
        ],
        ignore_conflicts=True,
    )


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "code",
                    models.CharField(max_length=3, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=80)),
                ("symbol", models.CharField(max_length=8)),
                ("decimal_places", models.PositiveSmallIntegerField(default=2)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["code"]},
        ),
        migrations.CreateModel(
            name="Trip",
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
                ("name", models.CharField(db_index=True, max_length=140)),
                (
                    "destination",
                    models.CharField(blank=True, db_index=True, max_length=160),
                ),
                ("description", models.TextField(blank=True)),
                ("trip_image", models.URLField(blank=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("planning", "Planning"),
                            ("active", "Active"),
                            ("closed", "Closed"),
                            ("archived", "Archived"),
                        ],
                        db_index=True,
                        default="planning",
                        max_length=20,
                    ),
                ),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "currency",
                    models.ForeignKey(
                        default="INR",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="trips.currency",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_trips",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TripMember",
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
                    "role",
                    models.CharField(
                        choices=[
                            ("owner", "Owner"),
                            ("admin", "Admin"),
                            ("member", "Member"),
                        ],
                        default="member",
                        max_length=20,
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="memberships",
                        to="trips.trip",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trip_memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"unique_together": {("trip", "user")}},
        ),
        migrations.CreateModel(
            name="TripInvitation",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                            ("cancelled", "Cancelled"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "invited_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "invited_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trip_invitations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to="trips.trip",
                    ),
                ),
            ],
            options={"unique_together": {("trip", "invited_user")}},
        ),
        migrations.RunPython(seed_currencies, migrations.RunPython.noop),
    ]
