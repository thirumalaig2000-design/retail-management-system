from django.urls import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import Role, User


class ReportPermissionsTests(APITestCase):
    def setUp(self):
        role, _ = Role.objects.get_or_create(code=Role.Code.USER, defaults={"label": "User"})
        self.user = User.objects.create_user(email="reports-user@example.com", password="SafePass!123", role=role)
        self.client.force_authenticate(self.user)

    def test_user_can_view_own_sales_report_but_not_inventory_report(self):
        self.assertEqual(self.client.get(reverse("reports-sales")).status_code, 200)
        self.assertEqual(self.client.get(reverse("reports-inventory")).status_code, 403)

    def test_dashboard_requires_authentication(self):
        self.client.force_authenticate(user=None)
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 401)
