from __future__ import annotations

from datetime import date

from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone

from apps.accounts.models import Role
from apps.inventory.models import Inventory
from apps.products.models import Product
from apps.purchases.models import Purchase, PurchaseItem
from apps.sales.models import Payment, Sale, SaleItem

MONEY = DecimalField(max_digits=14, decimal_places=2)


def _date_params(params):
    today = timezone.localdate()
    try:
        start = date.fromisoformat(params.get("start_date", str(today.replace(day=1))))
        end = date.fromisoformat(params.get("end_date", str(today)))
    except ValueError as exc:
        raise ValueError("Dates must use YYYY-MM-DD format.") from exc
    if start > end:
        raise ValueError("start_date cannot be after end_date.")
    return start, end


def _completed_sales(user=None):
    sales = Sale.objects.filter(status=Sale.Status.COMPLETED)
    if user and user.role.code == Role.Code.USER:
        sales = sales.filter(cashier=user)
    return sales


def _money(value):
    return value or 0


def dashboard_data(user):
    today = timezone.localdate()
    sales = _completed_sales(user)
    today_sales = sales.filter(created_at__date=today)
    month_sales = sales.filter(created_at__year=today.year, created_at__month=today.month)
    revenue = _money(sales.aggregate(value=Sum("grand_total"))["value"])
    cogs = _money(
        SaleItem.objects.filter(sale__in=sales).aggregate(
            value=Sum(ExpressionWrapper(F("quantity") * F("purchase_price_snapshot"), output_field=MONEY))
        )["value"]
    )
    daily_rows = (
        sales.filter(created_at__date__gte=today.replace(day=1))
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(revenue=Coalesce(Sum("grand_total"), 0, output_field=MONEY), orders=Sum(1))
        .order_by("day")
    )
    payload = {
        "role": user.role.code,
        "today_sales": _money(today_sales.aggregate(value=Sum("grand_total"))["value"]),
        "monthly_sales": _money(month_sales.aggregate(value=Sum("grand_total"))["value"]),
        "today_orders": today_sales.count(),
        "total_orders": sales.count(),
        "revenue": revenue,
        "gross_profit": revenue - cogs,
        "sales_chart": [{"date": row["day"].isoformat(), "revenue": row["revenue"], "orders": row["orders"]} for row in daily_rows],
        "top_products": product_sales_data(sales, limit=5),
    }
    if user.role.code != Role.Code.USER:
        payload.update({
            "total_products": Product.objects.filter(is_active=True).count(),
            "total_customers": sales.exclude(customer__isnull=True).values("customer").distinct().count(),
            "total_suppliers": Purchase.objects.values("supplier").distinct().count(),
            "total_purchases": Purchase.objects.count(),
            "low_stock": Inventory.objects.filter(current_stock__lte=F("product__minimum_stock")).count(),
        })
    return payload


def product_sales_data(sales, limit=None):
    rows = (
        SaleItem.objects.filter(sale__in=sales)
        .values("product_id", "product__name", "product__sku")
        .annotate(
            quantity=Coalesce(Sum("quantity"), 0, output_field=MONEY),
            revenue=Coalesce(Sum("total"), 0, output_field=MONEY),
        )
        .order_by("-quantity", "product__name")
    )
    if limit:
        rows = rows[:limit]
    return [
        {"product_id": row["product_id"], "name": row["product__name"], "sku": row["product__sku"], "quantity": row["quantity"], "revenue": row["revenue"]}
        for row in rows
    ]


def sales_report(user, params):
    start, end = _date_params(params)
    sales = _completed_sales(user).filter(created_at__date__range=(start, end))
    rows = sales.annotate(day=TruncDate("created_at")).values("day").annotate(
        orders=Sum(1), revenue=Coalesce(Sum("grand_total"), 0, output_field=MONEY),
        discount=Coalesce(Sum("discount"), 0, output_field=MONEY), tax=Coalesce(Sum("tax"), 0, output_field=MONEY),
    ).order_by("day")
    return {"start_date": start, "end_date": end, "summary": {"orders": sales.count(), "revenue": _money(sales.aggregate(value=Sum("grand_total"))["value"])}, "results": list(rows)}


def inventory_report():
    inventories = Inventory.objects.select_related("product", "product__category").all()
    results = [{"product_id": item.product_id, "name": item.product.name, "sku": item.product.sku, "category": item.product.category.name, "current_stock": item.current_stock, "minimum_stock": item.product.minimum_stock, "stock_value": item.current_stock * item.product.purchase_price, "is_low_stock": item.current_stock <= item.product.minimum_stock} for item in inventories]
    return {"summary": {"products": len(results), "low_stock": sum(item["is_low_stock"] for item in results), "stock_value": sum((item["stock_value"] for item in results), 0)}, "results": results}


def purchase_report(params):
    start, end = _date_params(params)
    purchases = Purchase.objects.filter(purchase_date__range=(start, end))
    return {"start_date": start, "end_date": end, "summary": {"orders": purchases.count(), "total": _money(purchases.aggregate(value=Sum("total"))["value"])}, "results": list(purchases.values("id", "purchase_number", "purchase_date", "status", "supplier__name", "subtotal", "tax", "total").order_by("-purchase_date"))}


def payment_report(user, params):
    start, end = _date_params(params)
    payments = Payment.objects.filter(payment_status=Payment.Status.PAID, created_at__date__range=(start, end))
    if user.role.code == Role.Code.USER:
        payments = payments.filter(sale__cashier=user)
    results = payments.values("payment_method").annotate(count=Sum(1), amount=Coalesce(Sum("amount"), 0, output_field=MONEY)).order_by("payment_method")
    return {"start_date": start, "end_date": end, "results": list(results)}


def profit_report(user, params):
    start, end = _date_params(params)
    sales = _completed_sales(user).filter(created_at__date__range=(start, end))
    revenue = _money(sales.aggregate(value=Sum("grand_total"))["value"])
    cogs = _money(SaleItem.objects.filter(sale__in=sales).aggregate(value=Sum(ExpressionWrapper(F("quantity") * F("purchase_price_snapshot"), output_field=MONEY)))["value"])
    return {"start_date": start, "end_date": end, "sales_revenue": revenue, "cost_of_goods_sold": cogs, "gross_profit": revenue - cogs}
