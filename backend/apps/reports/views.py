from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from apps.accounts.permissions import IsAdmin, IsUser

from . import services


class DashboardView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response(services.dashboard_data(request.user))


class ReportViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsUser]

    def _response(self, handler, request, admin_only=False):
        if admin_only and not IsAdmin().has_permission(request, self):
            return Response({"detail": "You do not have permission to view this report."}, status=status.HTTP_403_FORBIDDEN)
        try:
            return Response(handler(request.user, request.query_params) if handler in (services.sales_report, services.payment_report, services.profit_report) else handler(request.query_params) if handler is services.purchase_report else handler())
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc

    @action(detail=False, methods=["get"])
    def sales(self, request):
        return self._response(services.sales_report, request)

    @action(detail=False, methods=["get"])
    def products(self, request):
        try:
            start, end = services._date_params(request.query_params)
        except ValueError as exc:
            raise ValidationError({"detail": str(exc)}) from exc
        sales = services._completed_sales(request.user).filter(created_at__date__range=(start, end))
        return Response({"start_date": start, "end_date": end, "results": services.product_sales_data(sales)})

    @action(detail=False, methods=["get"])
    def inventory(self, request):
        return self._response(services.inventory_report, request, admin_only=True)

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        response = self._response(services.inventory_report, request, admin_only=True)
        if response.status_code == status.HTTP_200_OK:
            response.data["results"] = [item for item in response.data["results"] if item["is_low_stock"]]
        return response

    @action(detail=False, methods=["get"])
    def purchases(self, request):
        return self._response(services.purchase_report, request, admin_only=True)

    @action(detail=False, methods=["get"])
    def payments(self, request):
        return self._response(services.payment_report, request)

    @action(detail=False, methods=["get"])
    def profit(self, request):
        return self._response(services.profit_report, request, admin_only=True)
