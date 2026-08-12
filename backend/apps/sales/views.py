from __future__ import annotations

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.models import Role
from apps.accounts.permissions import IsAdmin, IsUser

from .models import Invoice, Payment, Sale
from .serializers import InvoiceSerializer, PaymentSerializer, SaleCompleteSerializer, SaleSerializer
from .services import complete_sale


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related("customer", "cashier").prefetch_related("items__product").all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["sale_number", "customer__name", "cashier__email", "status"]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        params = self.request.query_params
        status_param = params.get("status")
        if user.role.code == Role.Code.USER:
            queryset = queryset.filter(cashier=user)
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        sale = self.get_object()
        serializer = SaleCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            sale = complete_sale(
                sale=sale,
                payment_method=serializer.validated_data["payment_method"],
                transaction_reference=serializer.validated_data.get("transaction_reference", ""),
            )
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc
        return Response(self.get_serializer(sale).data, status=status.HTTP_200_OK)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.select_related("sale", "sale__customer", "sale__cashier").all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["sale__sale_number", "payment_method", "payment_status", "transaction_reference"]


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Invoice.objects.select_related("sale", "sale__customer", "sale__cashier", "sale__payment").all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["invoice_number", "sale__sale_number", "sale__customer__name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role.code == Role.Code.USER:
            queryset = queryset.filter(sale__cashier=self.request.user)
        return queryset
