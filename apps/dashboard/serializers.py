from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.dashboard.models import Dashboard, Widget


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
        fields = ["id", "configuration", "created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        dashboard_id = self.context.get("view").kwargs.get("dashboard_id")
        validated_data["dashboard"] = get_object_or_404(Dashboard, pk=dashboard_id)
        return super(WidgetSerializer, self).create(validated_data)


class UpdateWidgetListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        instance_map = {instance.pk: instance for instance in instances}
        data_updated = []

        for item in validated_data:
            id = item.get("id")
            instance = instance_map[id]
            data = {key: value for key, value in item.items() if key != "id"}
            self.child.update(instance, data)
            data_updated.append(instance)
        return data_updated


class UpdateWidgetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Widget
        fields = ["id", "configuration"]
        list_serializer_class = UpdateWidgetListSerializer

    def update(self, instance, validated_data):
        validated_data.pop("id", None)
        return super().update(instance, validated_data)
