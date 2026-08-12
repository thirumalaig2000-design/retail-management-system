from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from apps.accounts.permissions import IsAdmin, IsUser

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("name")
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "phone", "email", "address"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get("status")
        if status_param in {"active", "inactive"}:
            queryset = queryset.filter(is_active=status_param == "active")
        return queryset

    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.request.method == "POST":
            return [IsAuthenticated(), IsUser()]
        return [IsAuthenticated(), IsAdmin()]
