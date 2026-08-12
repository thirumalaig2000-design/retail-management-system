from django.contrib import admin

from .models import SystemSetting


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ("section", "key", "value", "updated_by", "updated_at")
    list_filter = ("section", "value_type", "is_editable")
    search_fields = ("key", "label", "value")
    readonly_fields = ("created_at", "updated_at")
