from django.core.validators import EmailValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import phone_validator


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    email = models.EmailField(blank=True, validators=[EmailValidator()])
    address = models.CharField(max_length=255, blank=True)
    tax_number = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return self.name
