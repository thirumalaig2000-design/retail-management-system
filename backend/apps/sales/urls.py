from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, PaymentViewSet, SaleViewSet

router = DefaultRouter()
router.register(r"sales", SaleViewSet, basename="sales")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"invoices", InvoiceViewSet, basename="invoices")

urlpatterns = router.urls
