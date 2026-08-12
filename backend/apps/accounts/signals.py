from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Role


@receiver(post_migrate)
def seed_default_roles(sender, **kwargs):
    if sender.name != "apps.accounts":
        return

    defaults = {
        Role.Code.SUPER_ADMIN: "Super Admin",
        Role.Code.ADMIN: "Admin",
        Role.Code.USER: "User",
    }
    for code, label in defaults.items():
        Role.objects.get_or_create(code=code, defaults={"label": label})
