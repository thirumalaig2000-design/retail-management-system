from django.contrib import admin

from .models import Invoice, Payment, Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("sale_number", "customer", "cashier", "status", "grand_total", "created_at")
    search_fields = ("sale_number", "customer__name", "cashier__email")
    list_filter = ("status", "created_at")
    inlines = [SaleItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("sale", "amount", "payment_method", "payment_status", "created_at")
    search_fields = ("sale__sale_number", "transaction_reference")
    list_filter = ("payment_method", "payment_status")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "sale", "payment_method", "issued_at")
    search_fields = ("invoice_number", "sale__sale_number")
