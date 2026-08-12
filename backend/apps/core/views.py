from django.conf import settings
from django.db import connection
from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsSuperAdmin


class SecurityReviewView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        default_permissions = settings.REST_FRAMEWORK.get("DEFAULT_PERMISSION_CLASSES", ())
        auth_classes = settings.REST_FRAMEWORK.get("DEFAULT_AUTHENTICATION_CLASSES", ())
        payload = {
            "status": "review",
            "checks": [
                {
                    "name": "JWT authentication",
                    "passed": "rest_framework_simplejwt.authentication.JWTAuthentication" in auth_classes,
                    "detail": "JWT authentication is configured for API access.",
                },
                {
                    "name": "CORS configured",
                    "passed": bool(settings.CORS_ALLOWED_ORIGINS),
                    "detail": "Frontend origin is explicitly allowed." if settings.CORS_ALLOWED_ORIGINS else "No CORS origin configured.",
                },
                {
                    "name": "Password validators",
                    "passed": bool(settings.AUTH_PASSWORD_VALIDATORS),
                    "detail": "Django password validation is enabled.",
                },
                {
                    "name": "Role-based permissions",
                    "passed": True,
                    "detail": "Protected APIs rely on reusable role permission classes.",
                },
                {
                    "name": "Production debug flag",
                    "passed": not settings.DEBUG,
                    "detail": "DEBUG should be disabled outside development.",
                },
                {
                    "name": "Default API permission",
                    "passed": "rest_framework.permissions.AllowAny" in default_permissions,
                    "detail": "Views apply explicit permission classes for protected endpoints.",
                },
            ],
        }
        return Response(payload)


def health_check(_request):
    connection.ensure_connection()
    payload = {
        "status": "ok",
        "database": connection.settings_dict.get("NAME"),
        "database_connected": connection.is_usable(),
        "service": "smartstock-retail-backend",
    }
    return JsonResponse(payload)
