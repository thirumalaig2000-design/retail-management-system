from __future__ import annotations

from rest_framework.permissions import BasePermission

from .models import User


class RolePermission(BasePermission):
    allowed_roles: tuple[str, ...] = ()

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if not isinstance(user, User):
            return False
        return user.role.code in self.allowed_roles


class IsSuperAdmin(RolePermission):
    allowed_roles = ("SUPER_ADMIN",)


class IsAdmin(RolePermission):
    allowed_roles = ("SUPER_ADMIN", "ADMIN")


class IsUser(RolePermission):
    allowed_roles = ("SUPER_ADMIN", "ADMIN", "USER")
