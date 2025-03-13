from dashboard.models import Dashboard, Widget
from django.contrib import admin


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "space",
        "created_at",
        "updated_at",
    )


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "configuration",
        "dashboard",
        "created_at",
        "updated_at",
    )
