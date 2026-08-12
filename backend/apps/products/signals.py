from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.inventory.models import Inventory

from .models import Product


@receiver(post_save, sender=Product)
def sync_inventory_for_product(sender, instance: Product, created: bool, **kwargs):
    Inventory.objects.update_or_create(
        product=instance,
        defaults={"current_stock": instance.current_stock},
    )
