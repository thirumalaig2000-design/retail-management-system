from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from .models import Supplier

User = get_user_model()


class SupplierApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="admin@smartstock.local",
            password="SmartStock!123",
            role=Role.objects.get(code=Role.Code.ADMIN),
        )
        self.user = User.objects.create_user(
            email="cashier@smartstock.local",
            password="SmartStock!123",
            role=Role.objects.get(code=Role.Code.USER),
        )

    def test_admin_can_create_suppliers(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/suppliers/",
            {
                "name": "Fresh Foods Ltd",
                "contact_person": "Maliha",
                "phone": "+8801811111111",
                "email": "contact@freshfoods.test",
                "address": "Chattogram",
                "tax_number": "TIN-12345",
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_manage_suppliers(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/suppliers/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
