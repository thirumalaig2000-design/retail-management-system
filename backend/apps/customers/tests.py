from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from .models import Customer

User = get_user_model()


class CustomerApiTests(TestCase):
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

    def test_user_can_create_customers(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/customers/",
            {
                "name": "Rahim Ahmed",
                "phone": "+8801711111111",
                "email": "rahim@example.com",
                "address": "Dhaka",
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_search_customers(self):
        Customer.objects.create(name="Rahim Ahmed", phone="+8801711111111", email="rahim@example.com")
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/customers/?search=rah")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
