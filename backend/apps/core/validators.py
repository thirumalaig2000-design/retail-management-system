from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^[0-9+\-\s()]{7,20}$",
    message="Enter a valid phone number.",
)
