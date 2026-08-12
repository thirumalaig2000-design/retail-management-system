from __future__ import annotations

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsAdmin

from .models import Purchase
from .serializers import PurchaseReceiveSerializer, PurchaseSerializer
from .services import receive_purchase


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.select_related("supplier", "created_by").prefetch_related("items__product").all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["purchase_number", "supplier__name", "status"]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        status_param = params.get("status")
        supplier_id = params.get("supplier")
        if status_param:
            queryset = queryset.filter(status=status_param)
        if supplier_id:
            queryset = queryset.filter(supplier_id=supplier_id)
        return queryset

    @action(detail=True, methods=["post"])
    def receive(self, request, pk=None):
        purchase = self.get_object()
        serializer = PurchaseReceiveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            purchase = receive_purchase(purchase=purchase, created_by=request.user)
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc
        return Response(self.get_serializer(purchase).data, status=status.HTTP_200_OK)
