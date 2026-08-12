from rest_framework import serializers

from .models import SystemSetting
from .services import normalize_setting_value


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = (
            "id",
            "key",
            "label",
            "section",
            "value",
            "value_type",
            "description",
            "is_editable",
            "updated_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "key", "label", "section", "value_type", "description", "created_at", "updated_at", "updated_by")

    def validate_value(self, value):
        setting = self.instance
        if not setting:
            return value
        if not setting.is_editable:
            raise serializers.ValidationError("This setting cannot be edited.")
        if setting.value_type == SystemSetting.ValueType.NUMBER:
            normalize_setting_value(setting, value)
        elif setting.value_type == SystemSetting.ValueType.BOOLEAN:
            normalize_setting_value(setting, value)
        return value

    def update(self, instance, validated_data):
        instance.value = normalize_setting_value(instance, validated_data.get("value", instance.value))
        instance.updated_by = self.context["request"].user
        instance.save(update_fields=["value", "updated_by", "updated_at"])
        return instance
