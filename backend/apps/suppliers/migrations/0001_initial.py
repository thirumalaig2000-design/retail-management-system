from django.core.validators import EmailValidator
from django.db import migrations, models
import apps.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Supplier",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
                ("contact_person", models.CharField(blank=True, max_length=150)),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        validators=[apps.core.validators.phone_validator],
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        validators=[EmailValidator()],
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255)),
                ("tax_number", models.CharField(blank=True, max_length=80)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["name"], name="suppliers_s_name_6277a9_idx"),
                    models.Index(fields=["phone"], name="suppliers_s_phone_af9b45_idx"),
                    models.Index(fields=["is_active"], name="suppliers_s_is_acti_a75d30_idx"),
                ],
            },
        ),
    ]
