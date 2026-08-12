from __future__ import annotations

from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import log_event
from apps.products.models import Product

from .models import Inventory, StockTransaction


def _ensure_inventory(product: Product) -> Inventory:
    inventory, _ = Inventory.objects.get_or_create(
        product=product,
        defaults={"current_stock": product.current_stock},
    )
    return inventory


def _record_transaction(
    *,
    product: Product,
    transaction_type: str,
    quantity: Decimal,
    previous_stock: Decimal,
    new_stock: Decimal,
    created_by,
    reference_type: str = "",
    reference_id: str = "",
    reason: str = "",
) -> StockTransaction:
    return StockTransaction.objects.create(
        product=product,
        transaction_type=transaction_type,
        quantity=quantity,
        previous_stock=previous_stock,
        new_stock=new_stock,
        created_by=created_by,
        reference_type=reference_type,
        reference_id=reference_id,
        reason=reason,
    )


@transaction.atomic
def adjust_stock(*, product: Product, quantity: Decimal, direction: str, created_by, reason: str = "") -> StockTransaction:
    inventory = _ensure_inventory(product)
    inventory = Inventory.objects.select_for_update().get(pk=inventory.pk)
    product = Product.objects.select_for_update().get(pk=product.pk)

    previous_stock = inventory.current_stock
    if direction == StockTransaction.TransactionType.ADJUSTMENT_IN:
        new_stock = previous_stock + quantity
    elif direction == StockTransaction.TransactionType.ADJUSTMENT_OUT:
        if previous_stock < quantity:
            raise ValueError("Insufficient stock for adjustment.")
        new_stock = previous_stock - quantity
    else:
        raise ValueError("Invalid stock adjustment direction.")

    inventory.current_stock = new_stock
    inventory.last_adjusted_at = timezone.now()
    inventory.save(update_fields=["current_stock", "last_adjusted_at", "updated_at"])

    product.current_stock = new_stock
    product.save(update_fields=["current_stock", "updated_at"])

    transaction_record = _record_transaction(
        product=product,
        transaction_type=direction,
        quantity=quantity,
        previous_stock=previous_stock,
        new_stock=new_stock,
        created_by=created_by,
        reason=reason,
    )
    log_event(
        user=created_by,
        action=AuditLog.Action.ADJUSTED,
        module=AuditLog.Module.INVENTORY,
        record_id=str(transaction_record.pk),
        description=f"Adjusted stock for {product.sku}: {reason or direction}.",
    )
    return transaction_record


@transaction.atomic
def increase_stock(*, product: Product, quantity: Decimal, created_by, reference_type: str = "", reference_id: str = "", reason: str = "") -> StockTransaction:
    inventory = _ensure_inventory(product)
    inventory = Inventory.objects.select_for_update().get(pk=inventory.pk)
    product = Product.objects.select_for_update().get(pk=product.pk)

    previous_stock = inventory.current_stock
    new_stock = previous_stock + quantity

    inventory.current_stock = new_stock
    inventory.last_adjusted_at = timezone.now()
    inventory.save(update_fields=["current_stock", "last_adjusted_at", "updated_at"])

    product.current_stock = new_stock
    product.save(update_fields=["current_stock", "updated_at"])

    return _record_transaction(
        product=product,
        transaction_type=StockTransaction.TransactionType.STOCK_IN,
        quantity=quantity,
        previous_stock=previous_stock,
        new_stock=new_stock,
        created_by=created_by,
        reference_type=reference_type,
        reference_id=reference_id,
        reason=reason,
    )


@transaction.atomic
def decrease_stock(*, product: Product, quantity: Decimal, created_by, reference_type: str = "", reference_id: str = "", reason: str = "") -> StockTransaction:
    inventory = _ensure_inventory(product)
    inventory = Inventory.objects.select_for_update().get(pk=inventory.pk)
    product = Product.objects.select_for_update().get(pk=product.pk)

    previous_stock = inventory.current_stock
    if previous_stock < quantity:
        raise ValueError("Insufficient stock.")
    new_stock = previous_stock - quantity

    inventory.current_stock = new_stock
    inventory.last_adjusted_at = timezone.now()
    inventory.save(update_fields=["current_stock", "last_adjusted_at", "updated_at"])

    product.current_stock = new_stock
    product.save(update_fields=["current_stock", "updated_at"])

    return _record_transaction(
        product=product,
        transaction_type=StockTransaction.TransactionType.STOCK_OUT,
        quantity=quantity,
        previous_stock=previous_stock,
        new_stock=new_stock,
        created_by=created_by,
        reference_type=reference_type,
        reference_id=reference_id,
        reason=reason,
    )
