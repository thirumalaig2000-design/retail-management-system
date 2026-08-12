from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class Sale(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    sale_number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales",
    )
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sales")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sale_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["cashier", "created_at"]),
        ]

    def __str__(self) -> str:
        return self.sale_number


class SaleItem(TimeStampedModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="sale_items")
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    purchase_price_snapshot = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
        indexes = [
            models.Index(fields=["sale", "product"]),
            models.Index(fields=["product"]),
        ]


class Payment(TimeStampedModel):
    class Method(models.TextChoices):
        CASH = "CASH", "Cash"
        CARD = "CARD", "Card"
        UPI = "UPI", "UPI"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=10, choices=Method.choices)
    payment_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_reference = models.CharField(max_length=100, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["payment_status"]),
            models.Index(fields=["payment_method"]),
            models.Index(fields=["created_at"]),
        ]


class Invoice(TimeStampedModel):
    invoice_number = models.CharField(max_length=30, unique=True)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name="invoice")
    issued_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=Payment.Method.choices)

    class Meta:
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["invoice_number"]),
            models.Index(fields=["issued_at"]),
        ]

    def __str__(self) -> str:
        return self.invoice_number
