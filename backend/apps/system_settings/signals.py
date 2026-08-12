from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .services import seed_default_settings


@receiver(post_migrate)
def seed_system_settings(sender, **kwargs):
    if sender.name != "apps.system_settings":
        return
    seed_default_settings()
