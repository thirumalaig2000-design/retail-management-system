from django.urls import path

from .views import InventoryAdjustmentViewSet, InventoryLowStockViewSet, InventoryViewSet, StockTransactionViewSet

inventory_list = InventoryViewSet.as_view({"get": "list"})
inventory_detail = InventoryViewSet.as_view({"get": "retrieve"})
transaction_list = StockTransactionViewSet.as_view({"get": "list"})
low_stock_list = InventoryLowStockViewSet.as_view({"get": "list"})
inventory_adjust = InventoryAdjustmentViewSet.as_view({"post": "create"})

urlpatterns = [
    path("inventory/", inventory_list, name="inventory-list"),
    path("inventory/<int:pk>/", inventory_detail, name="inventory-detail"),
    path("inventory/transactions/", transaction_list, name="inventory-transaction-list"),
    path("inventory/low-stock/", low_stock_list, name="inventory-low-stock-list"),
    path("inventory/adjust/", inventory_adjust, name="inventory-adjust"),
]
