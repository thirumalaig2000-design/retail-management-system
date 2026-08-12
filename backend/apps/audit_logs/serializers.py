from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "user",
            "user_email",
            "user_name",
            "action",
            "module",
            "record_id",
            "description",
            "created_at",
        )
        read_only_fields = fields
