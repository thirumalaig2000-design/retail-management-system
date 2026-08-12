from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Inventory",
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
                    "current_stock",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("last_adjusted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "product",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inventory",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "ordering": ["product__name"],
                "indexes": [
                    models.Index(fields=["current_stock"], name="inventory_i_current_13b727_idx"),
                    models.Index(fields=["product"], name="inventory_i_product_f4f8f8_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="StockTransaction",
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
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("STOCK_IN", "Stock In"),
                            ("STOCK_OUT", "Stock Out"),
                            ("SALE", "Sale"),
                            ("PURCHASE", "Purchase"),
                            ("ADJUSTMENT_IN", "Adjustment In"),
                            ("ADJUSTMENT_OUT", "Adjustment Out"),
                            ("RETURN", "Return"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                    ),
                ),
                ("previous_stock", models.DecimalField(decimal_places=2, max_digits=12)),
                ("new_stock", models.DecimalField(decimal_places=2, max_digits=12)),
                ("reference_type", models.CharField(blank=True, max_length=50)),
                ("reference_id", models.CharField(blank=True, max_length=50)),
                ("reason", models.CharField(blank=True, max_length=255)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="stock_transactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="stock_transactions",
                        to="products.product",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["product", "created_at"], name="inventory_s_product_0dfd3c_idx"),
                    models.Index(fields=["transaction_type"], name="inventory_s_transac_f888de_idx"),
                    models.Index(fields=["created_at"], name="inventory_s_created_ff5dbb_idx"),
                ],
                "constraints": [
                    models.CheckConstraint(condition=models.Q(quantity__gt=0), name="stocktxn_quantity_gt_0"),
                    models.CheckConstraint(condition=models.Q(previous_stock__gte=0), name="stocktxn_previous_stock_gte_0"),
                    models.CheckConstraint(condition=models.Q(new_stock__gte=0), name="stocktxn_new_stock_gte_0"),
                ],
            },
        ),
    ]
