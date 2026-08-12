from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("action", models.CharField(choices=[("LOGIN", "Login"), ("LOGOUT", "Logout"), ("CREATED", "Created"), ("UPDATED", "Updated"), ("DEACTIVATED", "Deactivated"), ("ADJUSTED", "Adjusted"), ("RECEIVED", "Received"), ("COMPLETED", "Completed"), ("SETTINGS_UPDATED", "Settings Updated")], max_length=30)),
                ("module", models.CharField(choices=[("AUTH", "Authentication"), ("PRODUCT", "Product"), ("CATEGORY", "Category"), ("CUSTOMER", "Customer"), ("SUPPLIER", "Supplier"), ("INVENTORY", "Inventory"), ("PURCHASE", "Purchase"), ("SALE", "Sale"), ("USER", "User"), ("SETTINGS", "Settings"), ("SECURITY", "Security")], max_length=30)),
                ("record_id", models.CharField(blank=True, max_length=80)),
                ("description", models.CharField(max_length=255)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="audit_logs", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["created_at"], name="audit_logs__created_0fc90a_idx"),
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["module", "created_at"], name="audit_logs__module_865b40_idx"),
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["action", "created_at"], name="audit_logs__action_70fdcf_idx"),
        ),
        migrations.AddIndex(
            model_name="auditlog",
            index=models.Index(fields=["user", "created_at"], name="audit_logs__user_id_d31e2a_idx"),
        ),
    ]
