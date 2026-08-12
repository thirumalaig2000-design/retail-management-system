from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DashboardView, ReportViewSet

router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="reports")

urlpatterns = [path("dashboard/", DashboardView.as_view(), name="dashboard")] + router.urls
