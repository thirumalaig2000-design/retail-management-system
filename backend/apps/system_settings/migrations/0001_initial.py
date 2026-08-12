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
            name="SystemSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("key", models.CharField(max_length=80, unique=True)),
                ("label", models.CharField(max_length=120)),
                ("section", models.CharField(max_length=80)),
                ("value", models.TextField(blank=True)),
                ("value_type", models.CharField(choices=[("TEXT", "Text"), ("NUMBER", "Number"), ("BOOLEAN", "Boolean")], default="TEXT", max_length=20)),
                ("description", models.CharField(blank=True, max_length=255)),
                ("is_editable", models.BooleanField(default=True)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="system_settings_updates", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["section", "key"],
            },
        ),
        migrations.AddIndex(
            model_name="systemsetting",
            index=models.Index(fields=["section", "key"], name="system_sett_section_194d95_idx"),
        ),
        migrations.AddIndex(
            model_name="systemsetting",
            index=models.Index(fields=["key"], name="system_sett_key_05d472_idx"),
        ),
    ]
