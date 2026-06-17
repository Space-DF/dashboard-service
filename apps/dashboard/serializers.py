import logging

from common.utils.telemetry_client import TelemetryServiceClient
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from apps.dashboard.models import Dashboard, Widget
from apps.dashboard.services import calculate_time_range, validate_widget_configuration

logger = logging.getLogger(__name__)
telemetry_client = TelemetryServiceClient()


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ["id", "name", "created_at", "updated_at"]
        extra_kwargs = {
            "id": {"read_only": True},
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
                logger.info(
                    f"Fetching telemetry data for widget: {instance.id}, organization: {request.tenant.slug_name}"
                )
                config = instance.configuration or {}
                start_time, end_time = calculate_time_range(config)
                data["data"] = telemetry_client.get_widget_data(
                    entity_id=instance.entity_id,
                    display_type=instance.display_type,
                    organization_slug=request.tenant.slug_name,
                    start_time=start_time,
                    end_time=end_time,
                )
                logger.info(
                    f"Successfully fetched telemetry data for widget: {instance.id}"
                )
            else:
                logger.warning("Organization slug_name is empty")
                data["data"] = {}
        except Exception as e:
            logger.exception(
                f"Unexpected error fetching widget data for {instance.id}: {str(e)}"
            )
            data["data"] = None

        return data

    def create(self, validated_data):
        dashboard_id = self.context.get("view").kwargs.get("dashboard_id")
        try:
            validated_data["dashboard"] = get_object_or_404(Dashboard, pk=dashboard_id)
            widget = super(WidgetSerializer, self).create(validated_data)
            logger.info(
                f"Successfully created widget: {widget.id} in dashboard: {dashboard_id}"
            )
            return widget
        except Exception as e:
            logger.error(
                f"Failed to create widget in dashboard {dashboard_id}: {str(e)}",
                exc_info=True,
            )
            raise


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
            try:
                Widget.objects.bulk_update(updated_instances, list(fields_to_update))
                logger.info(
                    f"Successfully bulk updated {len(updated_instances)} widgets with fields: {list(fields_to_update)}"
                )
            except Exception as e:
                logger.error(f"Failed to bulk update widgets: {str(e)}", exc_info=True)
                raise

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
