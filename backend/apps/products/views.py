from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from apps.accounts.permissions import IsAdmin
from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import log_event

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all().order_by("name")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "sku", "barcode", "brand", "category__name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        status_param = params.get("status")
        category_id = params.get("category")
        if status_param in {"active", "inactive"}:
            queryset = queryset.filter(is_active=status_param == "active")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdmin()]

    def perform_create(self, serializer):
        product = serializer.save()
        log_event(
            user=self.request.user,
            action=AuditLog.Action.CREATED,
            module=AuditLog.Module.PRODUCT,
            record_id=product.sku,
            description=f"Created product {product.name}.",
        )

    def perform_update(self, serializer):
        product = serializer.save()
        log_event(
            user=self.request.user,
            action=AuditLog.Action.UPDATED,
            module=AuditLog.Module.PRODUCT,
            record_id=product.sku,
            description=f"Updated product {product.name}.",
        )

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        product = self.get_object()
        product.is_active = True
        product.save(update_fields=["is_active", "updated_at"])
        log_event(
            user=request.user,
            action=AuditLog.Action.UPDATED,
            module=AuditLog.Module.PRODUCT,
            record_id=product.sku,
            description=f"Activated product {product.name}.",
        )
        return Response(self.get_serializer(product).data)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        product = self.get_object()
        product.is_active = False
        product.save(update_fields=["is_active", "updated_at"])
        log_event(
            user=request.user,
            action=AuditLog.Action.DEACTIVATED,
            module=AuditLog.Module.PRODUCT,
            record_id=product.sku,
            description=f"Deactivated product {product.name}.",
        )
        return Response(self.get_serializer(product).data)
