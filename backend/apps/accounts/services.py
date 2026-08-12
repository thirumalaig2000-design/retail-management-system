from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Role, User


@dataclass(frozen=True)
class AuthTokens:
    access: str
    refresh: str


def authenticate_user(*, email: str, password: str, request=None) -> User | None:
    return authenticate(request=request, username=email, email=email, password=password)


def build_tokens(user: User) -> AuthTokens:
    refresh = RefreshToken.for_user(user)
    return AuthTokens(access=str(refresh.access_token), refresh=str(refresh))


def get_role_for_creation(*, actor: User | None, requested_role_code: str | None) -> Role:
    target_code = requested_role_code or Role.Code.USER
    if actor and actor.role.code == Role.Code.ADMIN and target_code != Role.Code.USER:
        target_code = Role.Code.USER
    return Role.objects.get(code=target_code)


@transaction.atomic
def create_managed_user(*, actor: User | None, validated_data: dict) -> User:
    role = get_role_for_creation(
        actor=actor,
        requested_role_code=validated_data.pop("role_code", None),
    )
    password = validated_data.pop("password")
    user = User.objects.create_user(password=password, role=role, **validated_data)
    return user


@transaction.atomic
def update_managed_user(*, actor: User, user: User, validated_data: dict) -> User:
    requested_role_code = validated_data.pop("role_code", None)
    if requested_role_code:
        if actor.role.code != Role.Code.SUPER_ADMIN:
            requested_role_code = Role.Code.USER
        user.role = Role.objects.get(code=requested_role_code)

    for field in ("first_name", "last_name", "phone", "is_active"):
        if field in validated_data:
            setattr(user, field, validated_data[field])

    if "password" in validated_data and validated_data["password"]:
        user.set_password(validated_data["password"])

    user.save()
    return user


@transaction.atomic
def deactivate_user(*, actor: User, user: User) -> User:
    if user.role.code == Role.Code.SUPER_ADMIN:
        raise ValueError("SUPER_ADMIN users cannot be deactivated.")
    if actor.role.code != Role.Code.SUPER_ADMIN and user.role.code != Role.Code.USER:
        raise ValueError("Only SUPER_ADMIN can deactivate admin users.")
    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])
    return user
