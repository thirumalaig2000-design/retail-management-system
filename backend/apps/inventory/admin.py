from django.contrib import admin

from .models import Inventory, StockTransaction


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "current_stock", "last_adjusted_at", "updated_at")
    search_fields = ("product__name", "product__sku", "product__barcode")


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ("product", "transaction_type", "quantity", "previous_stock", "new_stock", "created_at")
    search_fields = ("product__name", "product__sku", "reference_type", "reference_id", "reason")
    list_filter = ("transaction_type", "created_at")
