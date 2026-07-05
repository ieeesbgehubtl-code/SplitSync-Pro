import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_categories(apps, schema_editor):
    Category = apps.get_model("expenses", "Category")
    for name in [
        "Food",
        "Hotel",
        "Transport",
        "Fuel",
        "Shopping",
        "Flight",
        "Train",
        "Entertainment",
        "Medical",
        "Emergency",
        "Cafe",
        "Snacks",
        "Other",
    ]:
        Category.objects.get_or_create(
            name=name, created_by=None, defaults={"is_system": True}
        )


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("trips", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=80)),
                ("icon", models.CharField(blank=True, max_length=40)),
                ("color", models.CharField(blank=True, max_length=20)),
                ("is_system", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["name"], "unique_together": {("name", "created_by")}},
        ),
        migrations.CreateModel(
            name="Expense",
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
                ("title", models.CharField(db_index=True, max_length=160)),
                ("description", models.TextField(blank=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("expense_date", models.DateField(db_index=True)),
                ("receipt_image", models.URLField(blank=True)),
                (
                    "split_method",
                    models.CharField(
                        choices=[
                            ("equal", "Equal"),
                            ("exact", "Exact"),
                            ("percentage", "Percentage"),
                            ("shares", "Shares"),
                            ("custom", "Custom"),
                        ],
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="expenses",
                        to="expenses.category",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_expenses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "paid_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="paid_expenses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "trip",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to="trips.trip",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="updated_expenses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExpenseParticipant",
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
                ("amount_owed", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "amount_paid",
                    models.DecimalField(decimal_places=2, default=0, max_digits=12),
                ),
                ("balance", models.DecimalField(decimal_places=2, max_digits=12)),
                ("split_type", models.CharField(max_length=20)),
                (
                    "share_percentage",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "share_units",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                (
                    "settlement_status",
                    models.CharField(
                        choices=[
                            ("open", "Open"),
                            ("partial", "Partial"),
                            ("settled", "Settled"),
                        ],
                        default="open",
                        max_length=20,
                    ),
                ),
                (
                    "expense",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participants",
                        to="expenses.expense",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expense_participants",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"unique_together": {("expense", "user")}},
        ),
        migrations.CreateModel(
            name="ExpenseComment",
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
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "expense",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="expenses.expense",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExpenseAudit",
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
                ("action", models.CharField(max_length=40)),
                ("before", models.JSONField(blank=True, default=dict)),
                ("after", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "actor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "expense",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audit_entries",
                        to="expenses.expense",
                    ),
                ),
            ],
        ),
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
