from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Role
from apps.categories.models import Category
from apps.customers.models import Customer
from apps.inventory.models import StockTransaction
from apps.products.models import Product
from .models import Invoice, Payment, Sale

User = get_user_model()


class SalesApiTests(TestCase):
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
        self.customer = Customer.objects.create(name="Rahim Ahmed", phone="+8801711111111", email="rahim@example.com")
        self.category = Category.objects.create(name="Beverages", description="Beverages")
        self.product = Product.objects.create(
            name="Tea Pack",
            sku="TEA-001",
            category=self.category,
            purchase_price=Decimal("40.00"),
            selling_price=Decimal("50.00"),
            tax_percentage=Decimal("5.00"),
            current_stock=Decimal("20.00"),
            minimum_stock=Decimal("5.00"),
            is_active=True,
        )

    def test_user_can_create_and_complete_sale(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/sales/",
            {
                "customer": self.customer.id,
                "discount": "5.00",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": "2.00",
                        "unit_price": "50.00",
                        "discount": "0.00",
                    }
                ],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sale_id = response.data["id"]
        complete = self.client.post(
            f"/api/sales/{sale_id}/complete/",
            {"payment_method": "CASH", "transaction_reference": "CASH-001"},
            format="json",
        )
        self.assertEqual(complete.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(str(self.product.current_stock), "18.00")
        self.assertEqual(Sale.objects.get(pk=sale_id).status, Sale.Status.COMPLETED)
        self.assertEqual(Payment.objects.filter(sale_id=sale_id).count(), 1)
        self.assertEqual(Invoice.objects.filter(sale_id=sale_id).count(), 1)
        self.assertEqual(StockTransaction.objects.filter(transaction_type="STOCK_OUT").count(), 1)

    def test_insufficient_stock_rejects_sale(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/sales/",
            {
                "customer": self.customer.id,
                "discount": "0.00",
                "items": [
                    {
                        "product": self.product.id,
                        "quantity": "200.00",
                        "unit_price": "50.00",
                        "discount": "0.00",
                    }
                ],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        complete = self.client.post(
            f"/api/sales/{response.data['id']}/complete/",
            {"payment_method": "CASH"},
            format="json",
        )
        self.assertEqual(complete.status_code, status.HTTP_400_BAD_REQUEST)
