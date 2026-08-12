from __future__ import annotations

from decimal import Decimal

from django.db import models, transaction
from django.utils import timezone

from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import log_event
from apps.inventory.services import decrease_stock
from apps.products.models import Product

from .models import Invoice, Payment, Sale, SaleItem


def _generate_sale_number() -> str:
    today = timezone.localdate().strftime("%Y%m%d")
    suffix = Sale.objects.count() + 1
    return f"SAL-{today}-{suffix:05d}"


def _generate_invoice_number() -> str:
    today = timezone.localdate().strftime("%Y%m%d")
    suffix = Invoice.objects.count() + 1
    return f"INV-{today}-{suffix:05d}"


def _recalculate_item_totals(quantity: Decimal, unit_price: Decimal, discount: Decimal, tax_percentage: Decimal) -> tuple[Decimal, Decimal, Decimal]:
    subtotal = quantity * unit_price
    taxable_base = max(Decimal("0"), subtotal - discount)
    tax = taxable_base * tax_percentage / Decimal("100")
    total = taxable_base + tax
    return subtotal, tax, total


@transaction.atomic
def create_sale(*, cashier, customer=None, discount=Decimal("0"), items_data: list[dict]) -> Sale:
    sale = Sale.objects.create(
        sale_number=_generate_sale_number(),
        cashier=cashier,
        customer=customer,
        discount=discount,
        subtotal=Decimal("0"),
        tax=Decimal("0"),
        grand_total=Decimal("0"),
        status=Sale.Status.PENDING,
    )

    for item in items_data:
        product = item["product"]
        quantity = Decimal(item["quantity"])
        item_discount = Decimal(item.get("discount", "0"))
        unit_price = Decimal(item.get("unit_price", product.selling_price))
        subtotal, tax, total = _recalculate_item_totals(quantity, unit_price, item_discount, product.tax_percentage)
        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            purchase_price_snapshot=product.purchase_price,
            discount=item_discount,
            tax=tax,
            subtotal=subtotal,
            total=total,
        )

    sale = recalculate_sale_totals(sale)
    log_event(
        user=cashier,
        action=AuditLog.Action.CREATED,
        module=AuditLog.Module.SALE,
        record_id=sale.sale_number,
        description=f"Created sale {sale.sale_number}.",
    )
    return sale


def recalculate_sale_totals(sale: Sale) -> Sale:
    totals = sale.items.aggregate(
        subtotal=models.Sum("subtotal"),
        tax=models.Sum("tax"),
        total=models.Sum("total"),
    )
    sale.subtotal = totals["subtotal"] or Decimal("0")
    sale.tax = totals["tax"] or Decimal("0")
    sale.grand_total = max(Decimal("0"), sale.subtotal - sale.discount + sale.tax)
    sale.save(update_fields=["subtotal", "tax", "grand_total", "updated_at"])
    return sale


@transaction.atomic
def complete_sale(*, sale: Sale, payment_method: str, transaction_reference: str = "") -> Sale:
    sale = Sale.objects.select_for_update().get(pk=sale.pk)
    if sale.status != Sale.Status.PENDING:
        raise ValueError("Only pending sales can be completed.")
    items = sale.items.select_related("product").all()
    if not items.exists():
        raise ValueError("Sale has no items.")

    recalculate_sale_totals(sale)

    for item in items:
        decrease_stock(
            product=item.product,
            quantity=item.quantity,
            created_by=sale.cashier,
            reference_type="SALE",
            reference_id=sale.sale_number,
            reason=f"Sale {sale.sale_number}",
        )

    Payment.objects.create(
        sale=sale,
        amount=sale.grand_total,
        payment_method=payment_method,
        payment_status=Payment.Status.PAID,
        transaction_reference=transaction_reference,
    )
    Invoice.objects.create(
        sale=sale,
        invoice_number=_generate_invoice_number(),
        payment_method=payment_method,
    )
    sale.status = Sale.Status.COMPLETED
    sale.save(update_fields=["status", "updated_at"])
    log_event(
        user=sale.cashier,
        action=AuditLog.Action.COMPLETED,
        module=AuditLog.Module.SALE,
        record_id=sale.sale_number,
        description=f"Completed sale {sale.sale_number}.",
    )
    return sale
