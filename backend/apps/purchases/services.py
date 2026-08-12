from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import log_event
from apps.inventory.services import increase_stock
from apps.products.models import Product

from .models import Purchase, PurchaseItem


def _generate_purchase_number() -> str:
    today = timezone.localdate().strftime("%Y%m%d")
    suffix = Purchase.objects.count() + 1
    return f"PUR-{today}-{suffix:05d}"


def _purchase_item_totals(quantity: Decimal, unit_price: Decimal, tax_percentage: Decimal) -> tuple[Decimal, Decimal, Decimal]:
    subtotal = quantity * unit_price
    tax = subtotal * tax_percentage / Decimal("100")
    total = subtotal + tax
    return subtotal, tax, total


@transaction.atomic
def create_purchase(*, supplier, created_by, purchase_date, status, items_data: list[dict]) -> Purchase:
    purchase = Purchase.objects.create(
        supplier=supplier,
        purchase_number=_generate_purchase_number(),
        purchase_date=purchase_date,
        status=status,
        created_by=created_by,
        subtotal=Decimal("0"),
        tax=Decimal("0"),
        total=Decimal("0"),
    )

    subtotal_total = Decimal("0")
    tax_total = Decimal("0")
    for item in items_data:
        product = item["product"]
        quantity = Decimal(item["quantity"])
        unit_price = Decimal(item.get("unit_price", product.purchase_price))
        tax_percentage = Decimal(item.get("tax_percentage", product.tax_percentage))
        subtotal, tax, total = _purchase_item_totals(quantity, unit_price, tax_percentage)
        PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            tax_percentage=tax_percentage,
            subtotal=subtotal,
            total=total,
        )
        subtotal_total += subtotal
        tax_total += tax

    purchase.subtotal = subtotal_total
    purchase.tax = tax_total
    purchase.total = subtotal_total + tax_total
    purchase.save(update_fields=["subtotal", "tax", "total", "updated_at"])
    log_event(
        user=created_by,
        action=AuditLog.Action.CREATED,
        module=AuditLog.Module.PURCHASE,
        record_id=purchase.purchase_number,
        description=f"Created purchase {purchase.purchase_number}.",
    )
    return purchase


@transaction.atomic
def receive_purchase(*, purchase: Purchase, created_by):
    purchase = Purchase.objects.select_for_update().get(pk=purchase.pk)
    if purchase.status != Purchase.Status.ORDERED:
        raise ValueError("Only ordered purchases can be received.")

    items = purchase.items.select_related("product").all()
    if not items.exists():
        raise ValueError("Purchase has no items.")

    for item in items:
        increase_stock(
            product=item.product,
            quantity=item.quantity,
            created_by=created_by,
            reference_type="PURCHASE",
            reference_id=purchase.purchase_number,
            reason=f"Received purchase {purchase.purchase_number}",
        )

    purchase.status = Purchase.Status.RECEIVED
    purchase.save(update_fields=["status", "updated_at"])
    log_event(
        user=created_by,
        action=AuditLog.Action.RECEIVED,
        module=AuditLog.Module.PURCHASE,
        record_id=purchase.purchase_number,
        description=f"Received purchase {purchase.purchase_number}.",
    )
    return purchase
