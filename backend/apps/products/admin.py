from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "is_active", "current_stock", "created_at")
    search_fields = ("name", "sku", "barcode", "brand", "category__name")
    list_filter = ("is_active", "category")
