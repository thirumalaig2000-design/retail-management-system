from __future__ import annotations

from django.db import models
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.accounts.models import Role
from apps.accounts.permissions import IsAdmin, IsUser
from apps.products.models import Product

from .models import Inventory, StockTransaction
from .serializers import InventorySerializer, StockAdjustmentSerializer, StockTransactionSerializer
from .services import adjust_stock


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.select_related("product", "product__category").all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__name", "product__sku", "product__barcode", "product__category__name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        low_stock = params.get("low_stock")
        category_id = params.get("category")
        if low_stock in {"1", "true", "True"}:
            queryset = queryset.filter(current_stock__lte=models.F("product__minimum_stock"))
        if category_id:
            queryset = queryset.filter(product__category_id=category_id)
        return queryset


class StockTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockTransaction.objects.select_related("product", "created_by", "product__category").all()
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["product__name", "product__sku", "reference_type", "reference_id", "reason", "transaction_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        product_id = params.get("product")
        transaction_type = params.get("type")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        return queryset


class InventoryAdjustmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=serializer.validated_data["product_id"])
        try:
            transaction = adjust_stock(
                product=product,
                quantity=serializer.validated_data["quantity"],
                direction=serializer.validated_data["direction"],
                created_by=request.user,
                reason=serializer.validated_data.get("reason", ""),
            )
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc
        return Response(StockTransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class InventoryLowStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.select_related("product", "product__category").all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(current_stock__lte=models.F("product__minimum_stock"))
