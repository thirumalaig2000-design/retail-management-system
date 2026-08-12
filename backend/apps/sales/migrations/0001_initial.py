from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("products", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
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
                ("sale_number", models.CharField(max_length=30, unique=True)),
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
                    "discount",
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
                    "grand_total",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                (
                    "cashier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sales",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="sales",
                        to="customers.customer",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CASH", "Cash"),
                            ("CARD", "Card"),
                            ("UPI", "UPI"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("PAID", "Paid"),
                            ("FAILED", "Failed"),
                            ("REFUNDED", "Refunded"),
                        ],
                        default="PENDING",
                        max_length=20,
                    ),
                ),
                ("transaction_reference", models.CharField(blank=True, max_length=100)),
                (
                    "sale",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to="sales.sale",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
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
                ("invoice_number", models.CharField(max_length=30, unique=True)),
                ("issued_at", models.DateTimeField(auto_now_add=True)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("CASH", "Cash"),
                            ("CARD", "Card"),
                            ("UPI", "UPI"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "sale",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invoice",
                        to="sales.sale",
                    ),
                ),
            ],
            options={
                "ordering": ["-issued_at"],
            },
        ),
        migrations.CreateModel(
            name="SaleItem",
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
                    "purchase_price_snapshot",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "discount",
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
                        related_name="sale_items",
                        to="products.product",
                    ),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="sales.sale",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(fields=["sale_number"], name="sales_sale_sale_nu_99d8fe_idx"),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(fields=["status"], name="sales_sale_status_532843_idx"),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(fields=["created_at"], name="sales_sale_created_e208b3_idx"),
        ),
        migrations.AddIndex(
            model_name="sale",
            index=models.Index(fields=["cashier", "created_at"], name="sales_sale_cashier_9d4ec1_idx"),
        ),
        migrations.AddIndex(
            model_name="payment",
            index=models.Index(fields=["payment_status"], name="sales_payme_payment_c95e1c_idx"),
        ),
        migrations.AddIndex(
            model_name="payment",
            index=models.Index(fields=["payment_method"], name="sales_payme_payment_b55c21_idx"),
        ),
        migrations.AddIndex(
            model_name="payment",
            index=models.Index(fields=["created_at"], name="sales_payme_created_0df64f_idx"),
        ),
        migrations.AddIndex(
            model_name="invoice",
            index=models.Index(fields=["invoice_number"], name="sales_invoi_invoice_51f3c9_idx"),
        ),
        migrations.AddIndex(
            model_name="invoice",
            index=models.Index(fields=["issued_at"], name="sales_invoi_issued__8c7d5a_idx"),
        ),
        migrations.AddIndex(
            model_name="saleitem",
            index=models.Index(fields=["sale", "product"], name="sales_salei_sale_id_17278e_idx"),
        ),
        migrations.AddIndex(
            model_name="saleitem",
            index=models.Index(fields=["product"], name="sales_salei_product_f87493_idx"),
        ),
    ]
