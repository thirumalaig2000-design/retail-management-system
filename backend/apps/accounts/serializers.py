from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Role, User
from .services import authenticate_user, build_tokens


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "code", "label", "description", "is_active")


class UserSummarySerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_code = serializers.CharField(source="role.code", read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "role",
            "role_code",
            "is_active",
            "is_staff",
            "date_joined",
        )


class UserWriteSerializer(serializers.ModelSerializer):
    role_code = serializers.ChoiceField(choices=Role.Code.choices, write_only=True)
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "role_code",
            "is_active",
        )
        read_only_fields = ("id",)

    def validate_email(self, value):
        normalized = value.lower().strip()
        if self.instance and self.instance.email == normalized:
            return normalized
        if User.objects.filter(email=normalized).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return normalized

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        actor = getattr(request, "user", None)
        if actor and actor.is_authenticated:
            requested_role = attrs.get("role_code", Role.Code.USER)
            if actor.role.code == Role.Code.ADMIN and requested_role != Role.Code.USER:
                raise serializers.ValidationError(
                    {"role_code": "Admins can only create or update USER accounts."}
                )
            if (
                self.instance
                and self.instance.role.code == Role.Code.SUPER_ADMIN
                and actor.role.code != Role.Code.SUPER_ADMIN
            ):
                raise serializers.ValidationError(
                    {"role_code": "Only SUPER_ADMIN can modify SUPER_ADMIN accounts."}
                )
        return attrs

    def create(self, validated_data):
        role_code = validated_data.pop("role_code")
        password = validated_data.pop("password")
        role = Role.objects.get(code=role_code)
        user = User.objects.create_user(password=password, role=role, **validated_data)
        return user

    def update(self, instance, validated_data):
        role_code = validated_data.pop("role_code", None)
        if role_code:
            instance.role = Role.objects.get(code=role_code)
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "role",
            "is_active",
        )
        read_only_fields = ("id", "email", "role", "is_active")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower().strip()
        password = attrs["password"]
        user = authenticate_user(email=email, password=password, request=self.context.get("request"))
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        tokens = build_tokens(user)
        self.user = user
        return {
            "access": tokens.access,
            "refresh": tokens.refresh,
            "user": UserSummarySerializer(user, context=self.context).data,
        }
