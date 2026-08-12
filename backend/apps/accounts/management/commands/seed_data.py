from __future__ import annotations

from django.core.management.base import BaseCommand

from apps.accounts.models import Role, User


SEED_PASSWORD = "SmartStock!123"


class Command(BaseCommand):
    help = "Seed development roles and demo users."

    def handle(self, *args, **options):
        roles = {
            Role.Code.SUPER_ADMIN: "Super Admin",
            Role.Code.ADMIN: "Admin",
            Role.Code.USER: "User",
        }
        for code, label in roles.items():
            Role.objects.update_or_create(code=code, defaults={"label": label, "is_active": True})

        demo_users = [
            {
                "email": "superadmin@smartstock.local",
                "role": Role.Code.SUPER_ADMIN,
                "first_name": "Super",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "email": "admin@smartstock.local",
                "role": Role.Code.ADMIN,
                "first_name": "Retail",
                "last_name": "Admin",
                "is_staff": False,
                "is_superuser": False,
            },
            {
                "email": "cashier@smartstock.local",
                "role": Role.Code.USER,
                "first_name": "Store",
                "last_name": "User",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for payload in demo_users:
            role = Role.objects.get(code=payload.pop("role"))
            user, created = User.objects.get_or_create(
                email=payload["email"],
                defaults={**payload, "role": role},
            )
            updated_fields = []
            if not created:
                for field, value in payload.items():
                    if getattr(user, field) != value:
                        setattr(user, field, value)
                        updated_fields.append(field)
            if user.role_id != role.id:
                user.role = role
                updated_fields.append("role")
            if created or not user.check_password(SEED_PASSWORD):
                user.set_password(SEED_PASSWORD)
                updated_fields.append("password")
            user.is_active = True
            updated_fields.append("is_active")
            user.save()

        self.stdout.write(self.style.SUCCESS("Development roles and users are ready."))
