import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=160)),
                ("sku", models.CharField(max_length=60, unique=True)),
                ("barcode", models.CharField(blank=True, max_length=80, null=True, unique=True)),
                ("brand", models.CharField(blank=True, max_length=120)),
                ("description", models.TextField(blank=True)),
                (
                    "purchase_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "selling_price",
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
                    "current_stock",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "minimum_stock",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="products/"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="categories.category",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "indexes": [
                    models.Index(fields=["sku"], name="products_pr_sku_ca0cdc_idx"),
                    models.Index(fields=["barcode"], name="products_pr_barcode_e44f4f_idx"),
                    models.Index(fields=["is_active"], name="products_pr_is_acti_ca4d9a_idx"),
                    models.Index(fields=["category", "is_active"], name="products_pr_categor_50f5f1_idx"),
                ],
                "constraints": [
                    models.CheckConstraint(condition=models.Q(purchase_price__gte=0), name="product_purchase_price_gte_0"),
                    models.CheckConstraint(condition=models.Q(selling_price__gte=0), name="product_selling_price_gte_0"),
                    models.CheckConstraint(condition=models.Q(tax_percentage__gte=0), name="product_tax_percentage_gte_0"),
                    models.CheckConstraint(condition=models.Q(current_stock__gte=0), name="product_current_stock_gte_0"),
                    models.CheckConstraint(condition=models.Q(minimum_stock__gte=0), name="product_minimum_stock_gte_0"),
                ],
            },
        ),
    ]
