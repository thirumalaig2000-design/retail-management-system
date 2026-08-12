from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from apps.categories.models import Category
from apps.products.models import Product
from .models import Inventory, StockTransaction

User = get_user_model()


class InventoryApiTests(TestCase):
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
        self.category = Category.objects.create(name="Staples", description="Staples")
        self.product = Product.objects.create(
            name="Rice 5kg",
            sku="RICE-5KG",
            barcode="8800001112223",
            category=self.category,
            purchase_price=Decimal("200.00"),
            selling_price=Decimal("240.00"),
            tax_percentage=Decimal("5.00"),
            current_stock=Decimal("20.00"),
            minimum_stock=Decimal("5.00"),
            is_active=True,
        )

    def test_inventory_list_is_available_to_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/inventory/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["current_stock"], "20.00")

    def test_admin_can_adjust_stock(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/inventory/adjust/",
            {
                "product_id": self.product.id,
                "quantity": "3.00",
                "direction": "ADJUSTMENT_OUT",
                "reason": "Damaged stock",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(str(self.product.current_stock), "17.00")
        self.assertEqual(StockTransaction.objects.count(), 1)
        self.assertEqual(Inventory.objects.get(product=self.product).current_stock, Decimal("17.00"))

    def test_insufficient_stock_is_blocked(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/inventory/adjust/",
            {
                "product_id": self.product.id,
                "quantity": "100.00",
                "direction": "ADJUSTMENT_OUT",
                "reason": "Too much",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
