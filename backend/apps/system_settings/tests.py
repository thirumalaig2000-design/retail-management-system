from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import Role
from .models import SystemSetting


class SystemSettingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        super_admin_role = Role.objects.get(code=Role.Code.SUPER_ADMIN)
        self.user = get_user_model().objects.create_user(
            email="super@example.com",
            password="password123",
            role=super_admin_role,
            is_staff=True,
        )

    def test_super_admin_can_list_settings(self):
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/settings/")

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["count"], 1)

    def test_super_admin_can_update_setting(self):
        self.client.force_authenticate(self.user)
        setting = SystemSetting.objects.get(key="store_name")

        response = self.client.patch(
            f"/api/settings/{setting.pk}/",
            {"value": "New SmartStock Store"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        setting.refresh_from_db()
        self.assertEqual(setting.value, "New SmartStock Store")
