from __future__ import annotations

from decimal import Decimal

from .models import SystemSetting


DEFAULT_SETTINGS = [
    {
        "key": "store_name",
        "label": "Store Name",
        "section": "Store",
        "value": "SmartStock Retail",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Display name used across the application.",
    },
    {
        "key": "store_address",
        "label": "Store Address",
        "section": "Store",
        "value": "",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Primary store address shown on invoices.",
    },
    {
        "key": "store_phone",
        "label": "Store Phone",
        "section": "Store",
        "value": "",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Main contact number for the business.",
    },
    {
        "key": "store_email",
        "label": "Store Email",
        "section": "Store",
        "value": "",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Primary contact email for the business.",
    },
    {
        "key": "currency",
        "label": "Currency",
        "section": "Finance",
        "value": "INR",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Currency code used for display.",
    },
    {
        "key": "tax_percentage",
        "label": "Tax Percentage",
        "section": "Finance",
        "value": "18",
        "value_type": SystemSetting.ValueType.NUMBER,
        "description": "Default tax percentage used in reports.",
    },
    {
        "key": "invoice_prefix",
        "label": "Invoice Prefix",
        "section": "Documents",
        "value": "INV",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Prefix used when generating invoice numbers.",
    },
    {
        "key": "low_stock_threshold",
        "label": "Low Stock Threshold",
        "section": "Inventory",
        "value": "10",
        "value_type": SystemSetting.ValueType.NUMBER,
        "description": "Items at or below this level are flagged as low stock.",
    },
    {
        "key": "business_timezone",
        "label": "Business Timezone",
        "section": "Store",
        "value": "Asia/Kolkata",
        "value_type": SystemSetting.ValueType.TEXT,
        "description": "Timezone used in reporting and date displays.",
    },
]


def seed_default_settings():
    for setting in DEFAULT_SETTINGS:
        SystemSetting.objects.get_or_create(
            key=setting["key"],
            defaults={k: v for k, v in setting.items() if k != "key"},
        )


def normalize_setting_value(setting: SystemSetting, value) -> str:
    if setting.value_type == SystemSetting.ValueType.BOOLEAN:
        return "true" if str(value).lower() in {"1", "true", "yes", "on"} else "false"
    if setting.value_type == SystemSetting.ValueType.NUMBER:
        return str(Decimal(str(value or 0)))
    return "" if value is None else str(value)
