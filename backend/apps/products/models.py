from django.core.validators import MinValueValidator
from django.db import models

from apps.categories.models import Category
from apps.core.models import TimeStampedModel


class Product(TimeStampedModel):
    name = models.CharField(max_length=160)
    sku = models.CharField(max_length=60, unique=True)
    barcode = models.CharField(max_length=80, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    minimum_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["category", "is_active"]),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(purchase_price__gte=0), name="product_purchase_price_gte_0"),
            models.CheckConstraint(condition=models.Q(selling_price__gte=0), name="product_selling_price_gte_0"),
            models.CheckConstraint(condition=models.Q(tax_percentage__gte=0), name="product_tax_percentage_gte_0"),
            models.CheckConstraint(condition=models.Q(current_stock__gte=0), name="product_current_stock_gte_0"),
            models.CheckConstraint(condition=models.Q(minimum_stock__gte=0), name="product_minimum_stock_gte_0"),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"
