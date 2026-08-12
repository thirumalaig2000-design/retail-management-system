from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from .models import Category

User = get_user_model()


class CategoryApiTests(TestCase):
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

    def test_admin_can_create_and_search_categories(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/categories/",
            {"name": "Beverages", "description": "Drinks", "is_active": True},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/categories/?search=bev")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_user_cannot_manage_categories(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
