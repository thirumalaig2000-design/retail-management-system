from decimal import Decimal

from rest_framework import serializers

from .models import Invoice, Payment, Sale, SaleItem
from .services import complete_sale, create_sale


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = SaleItem
        fields = (
            "id",
            "product",
            "product_name",
            "sku",
            "quantity",
            "unit_price",
            "purchase_price_snapshot",
            "discount",
            "tax",
            "subtotal",
            "total",
        )
        read_only_fields = ("id", "purchase_price_snapshot", "tax", "subtotal", "total", "product_name", "sku")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "sale", "amount", "payment_method", "payment_status", "transaction_reference", "created_at")
        read_only_fields = fields


class InvoiceSerializer(serializers.ModelSerializer):
    sale_number = serializers.CharField(source="sale.sale_number", read_only=True)
    customer_name = serializers.CharField(source="sale.customer.name", read_only=True)
    cashier_email = serializers.CharField(source="sale.cashier.email", read_only=True)
    payment_amount = serializers.DecimalField(source="sale.payment.amount", max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "invoice_number",
            "sale",
            "sale_number",
            "customer_name",
            "cashier_email",
            "payment_method",
            "payment_amount",
            "issued_at",
        )
        read_only_fields = fields


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    cashier_email = serializers.CharField(source="cashier.email", read_only=True)

    class Meta:
        model = Sale
        fields = (
            "id",
            "sale_number",
            "customer",
            "customer_name",
            "cashier",
            "cashier_email",
            "subtotal",
            "discount",
            "tax",
            "grand_total",
            "status",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "sale_number", "subtotal", "tax", "grand_total", "cashier", "created_at", "updated_at")

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one sale item is required.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        request = self.context["request"]
        discount = validated_data.get("discount", Decimal("0"))
        return create_sale(
            cashier=request.user,
            customer=validated_data.get("customer"),
            discount=discount,
            items_data=items_data,
        )


class SaleCompleteSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=Payment.Method.choices)
    transaction_reference = serializers.CharField(required=False, allow_blank=True, default="")
