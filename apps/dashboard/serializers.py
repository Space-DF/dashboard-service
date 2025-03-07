from apps.dashboard.models import Dashboard, Widget
from rest_framework import serializers
from rest_framework.generics import get_object_or_404


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "space": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "dashboard": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        dashboard_id = self.context.get("view").kwargs.get("dashboard_id")
        validated_data["dashboard"] = get_object_or_404(Dashboard, pk=dashboard_id)
        return super(WidgetSerializer, self).create(validated_data)
