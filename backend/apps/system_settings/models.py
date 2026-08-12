from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class SystemSetting(TimeStampedModel):
    class ValueType(models.TextChoices):
        TEXT = "TEXT", "Text"
        NUMBER = "NUMBER", "Number"
        BOOLEAN = "BOOLEAN", "Boolean"

    key = models.CharField(max_length=80, unique=True)
    label = models.CharField(max_length=120)
    section = models.CharField(max_length=80)
    value = models.TextField(blank=True)
    value_type = models.CharField(max_length=20, choices=ValueType.choices, default=ValueType.TEXT)
    description = models.CharField(max_length=255, blank=True)
    is_editable = models.BooleanField(default=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="system_settings_updates",
    )

    class Meta:
        ordering = ["section", "key"]
        indexes = [
            models.Index(fields=["section", "key"]),
            models.Index(fields=["key"]),
        ]

    def __str__(self) -> str:
        return self.label
