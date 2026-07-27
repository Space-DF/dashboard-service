from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0003_dashboard_is_deactivated"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboard",
            name="deactivated_at",
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
