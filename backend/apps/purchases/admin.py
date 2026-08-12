from django.contrib import admin

from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("purchase_number", "supplier", "status", "purchase_date", "total", "created_by")
    search_fields = ("purchase_number", "supplier__name")
    list_filter = ("status", "purchase_date")
    inlines = [PurchaseItemInline]


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("purchase", "product", "quantity", "unit_price", "total")
    search_fields = ("purchase__purchase_number", "product__name", "product__sku")
