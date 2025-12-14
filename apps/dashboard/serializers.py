from common.utils.telemetry_client import TelemetryServiceClient
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.dashboard.models import Dashboard, Widget
from apps.dashboard.services import validate_widget_configuration, calculate_time_range

telemetry_client = TelemetryServiceClient()


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
        fields = [
            "id",
            "display_type",
            "entity_id",
            "x",
            "y",
            "width",
            "height",
            "configuration",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, data):
        display_type = data.get("display_type")
        configuration = data.get("configuration") or {}
        validate_widget_configuration(display_type, configuration)
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)

        try:
            request = self.context.get("request")

            if request.tenant.slug_name:
                config = instance.configuration or {}
                
                # Calculate time range based on configuration
                # Returns (start_time, end_time) as ISO format strings
                start_time, end_time = calculate_time_range(config)

                data["data"] = telemetry_client.get_widget_data(
                    entity_id=instance.entity_id,
                    display_type=instance.display_type,
                    organization_slug=request.tenant.slug_name,
                    start_time=start_time,
                    end_time=end_time,
                )
            else:
                data["data"] = {}
        except Exception as e:
            data["data"] = {"error": str(e)}

        return data

    def create(self, validated_data):
        dashboard_id = self.context.get("view").kwargs.get("dashboard_id")
        validated_data["dashboard"] = get_object_or_404(Dashboard, pk=dashboard_id)
        return super(WidgetSerializer, self).create(validated_data)


class UpdateWidgetListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        instance_map = {instance.pk: instance for instance in instances}
        fields_to_update = set()
        updated_instances = []

        for item in validated_data:
            instance = instance_map[item["id"]]
            widget_updates = {key: value for key, value in item.items() if key != "id"}

            for key, value in widget_updates.items():
                setattr(instance, key, value)

            fields_to_update.update(widget_updates.keys())
            updated_instances.append(instance)

        if updated_instances:
            Widget.objects.bulk_update(updated_instances, list(fields_to_update))

        return updated_instances


class UpdateWidgetSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = Widget
        fields = [
            "id",
            "x",
            "y",
            "width",
            "height",
            "configuration",
        ]
        list_serializer_class = UpdateWidgetListSerializer

    def validate(self, data):
        instance = self.instance
        if instance and hasattr(instance, "display_type"):
            display_type = instance.display_type
        else:
            return data

        configuration = (
            data.get("configuration") or getattr(instance, "configuration", {}) or {}
        )
        validate_widget_configuration(display_type, configuration)
        return data

    def update(self, instance, validated_data):
        validated_data.pop("id", None)
        return super().update(instance, validated_data)
