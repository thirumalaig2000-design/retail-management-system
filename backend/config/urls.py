from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.core.urls")),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.categories.urls")),
    path("api/", include("apps.products.urls")),
    path("api/", include("apps.customers.urls")),
    path("api/", include("apps.suppliers.urls")),
    path("api/", include("apps.inventory.urls")),
    path("api/", include("apps.purchases.urls")),
    path("api/", include("apps.sales.urls")),
    path("api/", include("apps.reports.urls")),
    path("api/", include("apps.audit_logs.urls")),
    path("api/", include("apps.system_settings.urls")),
]
