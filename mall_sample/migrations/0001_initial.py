# Generated by Django 4.2.7 on 2023-11-23 20:29

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("name", models.CharField(max_length=50)),
                (
                    "amount",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, message="give me the money(than 1)"
                            )
                        ]
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ready", "미결제"),
                            ("paid", "결제완료"),
                            ("cancelled", "결제취소"),
                            ("failed", "결제실패"),
                        ],
                        db_index=True,
                        default="ready",
                        max_length=10,
                    ),
                ),
                (
                    "is_paid_ok",
                    models.BooleanField(db_index=True, default=False, editable=False),
                ),
            ],
        ),
    ]
