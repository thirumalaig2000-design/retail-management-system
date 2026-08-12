from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class Inventory(TimeStampedModel):
    product = models.OneToOneField("products.Product", on_delete=models.CASCADE, related_name="inventory")
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    last_adjusted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["product__name"]
        indexes = [
            models.Index(fields=["current_stock"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self) -> str:
        return f"Inventory for {self.product.sku}"


class StockTransaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        STOCK_IN = "STOCK_IN", "Stock In"
        STOCK_OUT = "STOCK_OUT", "Stock Out"
        SALE = "SALE", "Sale"
        PURCHASE = "PURCHASE", "Purchase"
        ADJUSTMENT_IN = "ADJUSTMENT_IN", "Adjustment In"
        ADJUSTMENT_OUT = "ADJUSTMENT_OUT", "Adjustment Out"
        RETURN = "RETURN", "Return"

    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="stock_transactions")
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    previous_stock = models.DecimalField(max_digits=12, decimal_places=2)
    new_stock = models.DecimalField(max_digits=12, decimal_places=2)
    reference_type = models.CharField(max_length=50, blank=True)
    reference_id = models.CharField(max_length=50, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="stock_transactions")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "created_at"]),
            models.Index(fields=["transaction_type"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name="stocktxn_quantity_gt_0"),
            models.CheckConstraint(condition=models.Q(previous_stock__gte=0), name="stocktxn_previous_stock_gte_0"),
            models.CheckConstraint(condition=models.Q(new_stock__gte=0), name="stocktxn_new_stock_gte_0"),
        ]

    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.product.sku}"
