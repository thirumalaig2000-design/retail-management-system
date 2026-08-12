from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "module", "action", "record_id")
    list_filter = ("module", "action", "created_at")
    search_fields = ("description", "record_id", "user__email")
    readonly_fields = [field.name for field in AuditLog._meta.fields]
