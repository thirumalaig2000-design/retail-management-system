from django.core.validators import RegexValidator
from django.db import migrations, models
import django.db.models.deletion
import apps.accounts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "code",
                    models.CharField(
                        choices=[
                            ("SUPER_ADMIN", "Super Admin"),
                            ("ADMIN", "Admin"),
                            ("USER", "User"),
                        ],
                        max_length=20,
                        unique=True,
                    ),
                ),
                ("label", models.CharField(max_length=50)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["code"],
                "indexes": [models.Index(fields=["code"], name="accounts_ro_code_5aeee6_idx")],
            },
        ),
        migrations.CreateModel(
            name="User",
            managers=[
                ("objects", apps.accounts.models.UserManager()),
            ],
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "email",
                    models.EmailField(max_length=254, unique=True),
                ),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        validators=[
                            RegexValidator(
                                message="Enter a valid phone number.",
                                regex=r"^[0-9+\-\s()]{7,20}$",
                            )
                        ],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text=(
                            "Designates that this user has all permissions without explicitly "
                            "assigning them."
                        ),
                        verbose_name="superuser status",
                    ),
                ),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text=(
                            "The groups this user belongs to. A user will get all permissions "
                            "granted to each of their groups."
                        ),
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="users",
                        to="accounts.role",
                    ),
                ),
            ],
            options={
                "ordering": ["email"],
                "indexes": [
                    models.Index(fields=["email"], name="accounts_us_email_74c8d6_idx"),
                    models.Index(fields=["role", "is_active"], name="accounts_us_role_id_85449e_idx"),
                ],
            },
        ),
    ]
