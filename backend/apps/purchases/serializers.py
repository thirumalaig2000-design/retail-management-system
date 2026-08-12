from rest_framework import serializers

from apps.products.models import Product
from apps.suppliers.models import Supplier

from .models import Purchase, PurchaseItem
from .services import create_purchase


class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    sku = serializers.CharField(source="product.sku", read_only=True)

    class Meta:
        model = PurchaseItem
        fields = ("id", "product", "product_name", "sku", "quantity", "unit_price", "tax_percentage", "subtotal", "total")
        read_only_fields = ("id", "subtotal", "total", "product_name", "sku")


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)

    class Meta:
        model = Purchase
        fields = (
            "id",
            "supplier",
            "supplier_name",
            "purchase_number",
            "purchase_date",
            "status",
            "subtotal",
            "tax",
            "total",
            "created_by",
            "created_by_email",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "purchase_number", "subtotal", "tax", "total", "created_by", "created_at", "updated_at")

    def validate_status(self, value):
        if value not in {Purchase.Status.DRAFT, Purchase.Status.ORDERED}:
            raise serializers.ValidationError("Purchase can only be created as draft or ordered.")
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one purchase item is required.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        request = self.context["request"]
        return create_purchase(
            supplier=validated_data["supplier"],
            created_by=request.user,
            purchase_date=validated_data["purchase_date"],
            status=validated_data.get("status", Purchase.Status.DRAFT),
            items_data=items_data,
        )


class PurchaseReceiveSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_blank=True, default="")
