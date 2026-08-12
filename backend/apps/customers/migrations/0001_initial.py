from django.core.validators import EmailValidator
from django.db import migrations, models
import apps.core.validators


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["name"], name="customers_c_name_f018e2_idx"),
                    models.Index(fields=["phone"], name="customers_c_phone_8493fa_idx"),
                    models.Index(fields=["is_active"], name="customers_c_is_acti_91d305_idx"),
                ],
            },
        ),
    ]
