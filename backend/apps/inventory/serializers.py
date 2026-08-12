from decimal import Decimal

from django.core.validators import MinValueValidator
from rest_framework import serializers

from apps.products.serializers import ProductSerializer

from .models import Inventory, StockTransaction


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)
    low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = ("id", "product", "product_id", "current_stock", "last_adjusted_at", "low_stock", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at", "last_adjusted_at", "low_stock")

    def get_low_stock(self, obj):
        return obj.current_stock <= obj.product.minimum_stock


class StockTransactionSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source="product.sku", read_only=True)
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)

    class Meta:
        model = StockTransaction
        fields = (
            "id",
            "product",
            "product_sku",
            "transaction_type",
            "quantity",
            "previous_stock",
            "new_stock",
            "reference_type",
            "reference_id",
            "reason",
            "created_by",
            "created_by_email",
            "created_at",
        )
        read_only_fields = ("id", "previous_stock", "new_stock", "created_by", "created_at")


class StockAdjustmentSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    direction = serializers.ChoiceField(
        choices=(
            ("ADJUSTMENT_IN", "ADJUSTMENT_IN"),
            ("ADJUSTMENT_OUT", "ADJUSTMENT_OUT"),
        )
    )
    reason = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_product_id(self, value):
        from apps.products.models import Product

        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Product not found.")
        return value
