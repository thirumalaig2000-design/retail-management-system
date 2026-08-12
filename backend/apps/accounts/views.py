from __future__ import annotations

from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import log_event

from .models import Role, User
from .permissions import IsAdmin, IsSuperAdmin
from .serializers import (
    LoginSerializer,
    ProfileSerializer,
    RoleSerializer,
    UserSummarySerializer,
    UserWriteSerializer,
)
from .services import deactivate_user


class LoginView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = getattr(serializer, "user", None)
        if user:
            log_event(
                user=user,
                action=AuditLog.Action.LOGIN,
                module=AuditLog.Module.AUTH,
                record_id=str(user.pk),
                description=f"{user.email} logged in.",
            )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):
    permission_classes = []


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            raise ValidationError({"refresh": _("This field is required.")})
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            log_event(
                user=request.user,
                action=AuditLog.Action.LOGOUT,
                module=AuditLog.Module.AUTH,
                record_id=str(request.user.pk),
                description=f"{request.user.email} logged out.",
            )
        except TokenError as exc:
            raise ValidationError({"refresh": str(exc)}) from exc
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["code", "label"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("role").all().order_by("email")
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name", "phone", "role__code"]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.action in {"create", "update", "partial_update"}:
            return UserWriteSerializer
        return UserSummarySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.role.code == Role.Code.ADMIN:
            return queryset.exclude(role__code=Role.Code.SUPER_ADMIN)
        return queryset

    def perform_create(self, serializer):
        user = serializer.save()
        log_event(
            user=self.request.user,
            action=AuditLog.Action.CREATED,
            module=AuditLog.Module.USER,
            record_id=str(user.pk),
            description=f"Created user {user.email}.",
        )

    def perform_update(self, serializer):
        user = serializer.save()
        log_event(
            user=self.request.user,
            action=AuditLog.Action.UPDATED,
            module=AuditLog.Module.USER,
            record_id=str(user.pk),
            description=f"Updated user {user.email}.",
        )

    def perform_destroy(self, instance):
        actor = self.request.user
        if instance.role.code == Role.Code.SUPER_ADMIN:
            raise ValidationError({"detail": "SUPER_ADMIN users cannot be deleted."})
        if actor.role.code != Role.Code.SUPER_ADMIN and instance.role.code != Role.Code.USER:
            raise ValidationError({"detail": "Admins can only delete USER accounts."})
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        log_event(
            user=actor,
            action=AuditLog.Action.DEACTIVATED,
            module=AuditLog.Module.USER,
            record_id=str(instance.pk),
            description=f"Deactivated user {instance.email}.",
        )

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        try:
            deactivate_user(actor=request.user, user=user)
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc
        log_event(
            user=request.user,
            action=AuditLog.Action.DEACTIVATED,
            module=AuditLog.Module.USER,
            record_id=str(user.pk),
            description=f"Deactivated user {user.email}.",
        )
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)
