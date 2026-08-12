from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsAdmin

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get("status")
        if status_param in {"active", "inactive"}:
            queryset = queryset.filter(is_active=status_param == "active")
        return queryset

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        category = self.get_object()
        category.is_active = True
        category.save(update_fields=["is_active", "updated_at"])
        return Response(self.get_serializer(category).data)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        category = self.get_object()
        category.is_active = False
        category.save(update_fields=["is_active", "updated_at"])
        return Response(self.get_serializer(category).data)
