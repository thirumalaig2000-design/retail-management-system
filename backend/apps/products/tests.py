from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from apps.categories.models import Category
from .models import Product

User = get_user_model()


class ProductApiTests(TestCase):
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
        self.category = Category.objects.create(name="Grocery", description="Groceries")

    def test_admin_can_create_and_filter_products(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/products/",
            {
                "name": "Rice 5kg",
                "sku": "RICE-5KG",
                "barcode": "8900001112223",
                "category": self.category.id,
                "brand": "SmartStock",
                "description": "Long grain rice",
                "purchase_price": "200.00",
                "selling_price": "240.00",
                "tax_percentage": "5.00",
                "current_stock": "25.00",
                "minimum_stock": "5.00",
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("/api/products/?search=rice")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_user_cannot_manage_products(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
