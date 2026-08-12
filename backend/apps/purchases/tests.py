from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from apps.categories.models import Category
from apps.inventory.models import StockTransaction
from apps.products.models import Product
from apps.suppliers.models import Supplier

from .models import Purchase

User = get_user_model()


class PurchasesApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            email="admin@smartstock.local",
            password="SmartStock!123",
            role=Role.objects.get(code=Role.Code.ADMIN),
        )
        self.supplier = Supplier.objects.create(name="Global Traders")
        self.category = Category.objects.create(name="Stationery", description="Stationery")
        self.product = Product.objects.create(
            name="Notebook",
            sku="NOTE-001",
            category=self.category,
            purchase_price=Decimal("20.00"),
            selling_price=Decimal("30.00"),
            tax_percentage=Decimal("5.00"),
            current_stock=Decimal("10.00"),
            minimum_stock=Decimal("3.00"),
            is_active=True,
        )

    def test_admin_can_create_and_receive_purchase(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/purchases/",
            {
                "supplier": self.supplier.id,
                "purchase_date": "2026-08-12",
                "status": "ORDERED",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": "5.00",
                        "unit_price": "20.00",
                        "tax_percentage": "5.00",
                    }
                ],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        purchase_id = response.data["id"]
        receive = self.client.post(f"/api/purchases/{purchase_id}/receive/", {"note": "Received"}, format="json")
        self.assertEqual(receive.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(str(self.product.current_stock), "15.00")
        self.assertEqual(Purchase.objects.get(pk=purchase_id).status, Purchase.Status.RECEIVED)
        self.assertEqual(StockTransaction.objects.filter(transaction_type="STOCK_IN").count(), 1)
