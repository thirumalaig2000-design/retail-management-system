from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import IsSuperAdmin
from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import log_event

from .models import SystemSetting
from .serializers import SystemSettingSerializer


class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.select_related("updated_by").all()
    serializer_class = SystemSettingSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["key", "label", "section", "description", "value"]
    ordering_fields = ["section", "key", "updated_at"]
    ordering = ["section", "key"]

    def perform_update(self, serializer):
        setting = serializer.save()
        log_event(
            user=self.request.user,
            action=AuditLog.Action.SETTINGS_UPDATED,
            module=AuditLog.Module.SETTINGS,
            record_id=setting.key,
            description=f"Updated {setting.label}.",
        )
