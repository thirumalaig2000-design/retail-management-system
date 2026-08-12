from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class AuditLog(TimeStampedModel):
    class Action(models.TextChoices):
        LOGIN = "LOGIN", "Login"
        LOGOUT = "LOGOUT", "Logout"
        CREATED = "CREATED", "Created"
        UPDATED = "UPDATED", "Updated"
        DEACTIVATED = "DEACTIVATED", "Deactivated"
        ADJUSTED = "ADJUSTED", "Adjusted"
        RECEIVED = "RECEIVED", "Received"
        COMPLETED = "COMPLETED", "Completed"
        SETTINGS_UPDATED = "SETTINGS_UPDATED", "Settings Updated"

    class Module(models.TextChoices):
        AUTH = "AUTH", "Authentication"
        PRODUCT = "PRODUCT", "Product"
        CATEGORY = "CATEGORY", "Category"
        CUSTOMER = "CUSTOMER", "Customer"
        SUPPLIER = "SUPPLIER", "Supplier"
        INVENTORY = "INVENTORY", "Inventory"
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"
        USER = "USER", "User"
        SETTINGS = "SETTINGS", "Settings"
        SECURITY = "SECURITY", "Security"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    action = models.CharField(max_length=30, choices=Action.choices)
    module = models.CharField(max_length=30, choices=Module.choices)
    record_id = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["module", "created_at"]),
            models.Index(fields=["action", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.module} {self.action} {self.record_id}".strip()
