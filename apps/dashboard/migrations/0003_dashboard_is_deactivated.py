from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_widget_display_type_widget_entity_id_widget_height_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboard",
            name="is_deactivated",
            field=models.BooleanField(default=False),
        ),
    ]
