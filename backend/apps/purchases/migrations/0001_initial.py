from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("suppliers", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Purchase",
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
                ("purchase_number", models.CharField(max_length=30, unique=True)),
                ("purchase_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("ORDERED", "Ordered"),
                            ("RECEIVED", "Received"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="DRAFT",
                        max_length=20,
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="purchases",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="purchases",
                        to="suppliers.supplier",
                    ),
                ),
            ],
            options={
                "ordering": ["-purchase_date", "-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PurchaseItem",
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
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                    ),
                ),
                (
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "tax_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="purchase_items",
                        to="products.product",
                    ),
                ),
                (
                    "purchase",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="purchases.purchase",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="purchase",
            index=models.Index(fields=["purchase_number"], name="purchases_p_purchas_12ae8f_idx"),
        ),
        migrations.AddIndex(
            model_name="purchase",
            index=models.Index(fields=["status"], name="purchases_p_status_0434fa_idx"),
        ),
        migrations.AddIndex(
            model_name="purchase",
            index=models.Index(fields=["purchase_date"], name="purchases_p_purchas_f942b0_idx"),
        ),
        migrations.AddIndex(
            model_name="purchase",
            index=models.Index(fields=["created_by", "purchase_date"], name="purchases_p_created_da4bec_idx"),
        ),
        migrations.AddIndex(
            model_name="purchaseitem",
            index=models.Index(fields=["purchase", "product"], name="purchases_p_purchas_00688d_idx"),
        ),
        migrations.AddIndex(
            model_name="purchaseitem",
            index=models.Index(fields=["product"], name="purchases_p_product_52a9a3_idx"),
        ),
    ]
