from rest_framework import serializers

from apps.categories.models import Category
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "barcode",
            "category",
            "category_name",
            "brand",
            "description",
            "purchase_price",
            "selling_price",
            "tax_percentage",
            "current_stock",
            "minimum_stock",
            "is_active",
            "image",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        sku = attrs.get("sku")
        barcode = attrs.get("barcode")
        if sku:
            normalized = sku.strip()
            if self.instance and self.instance.sku == normalized:
                attrs["sku"] = normalized
            elif Product.objects.filter(sku__iexact=normalized).exists():
                raise serializers.ValidationError({"sku": "Product with this SKU already exists."})
            else:
                attrs["sku"] = normalized

        if barcode:
            normalized_barcode = barcode.strip()
            if self.instance and self.instance.barcode == normalized_barcode:
                attrs["barcode"] = normalized_barcode
            elif Product.objects.filter(barcode__iexact=normalized_barcode).exists():
                raise serializers.ValidationError(
                    {"barcode": "Product with this barcode already exists."}
                )
            else:
                attrs["barcode"] = normalized_barcode

        return attrs
