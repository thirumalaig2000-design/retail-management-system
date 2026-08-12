from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SystemSettingViewSet

router = DefaultRouter()
router.register(r"settings", SystemSettingViewSet, basename="settings")

urlpatterns = router.urls
