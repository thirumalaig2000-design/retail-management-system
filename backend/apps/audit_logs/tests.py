from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import Role
from .models import AuditLog
from .services import log_event


class AuditLogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.super_admin_role = Role.objects.get(code=Role.Code.SUPER_ADMIN)
        self.user = get_user_model().objects.create_user(
            email="admin@example.com",
            password="password123",
            role=self.super_admin_role,
            is_staff=True,
        )

    def test_log_event_creates_record(self):
        log = log_event(
            user=self.user,
            action=AuditLog.Action.CREATED,
            module=AuditLog.Module.PRODUCT,
            record_id="P-1",
            description="Created product P-1.",
        )

        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertEqual(log.user, self.user)

    def test_admin_can_list_audit_logs(self):
        log_event(
            user=self.user,
            action=AuditLog.Action.LOGIN,
            module=AuditLog.Module.AUTH,
            record_id=str(self.user.pk),
            description="Logged in.",
        )
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/audit-logs/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
