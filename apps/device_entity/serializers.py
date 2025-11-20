from rest_framework import serializers

from apps.device_entity.models import EntityType, DeviceEntity
from apps.dashboard.models import Widget


class DeviceEntityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityType
        fields = ["id", "name", "description"]


class DeviceEntitiesSerializer(serializers.ModelSerializer):
    entity_type_id = serializers.PrimaryKeyRelatedField(queryset=EntityType.objects.all())
    widget_id = serializers.PrimaryKeyRelatedField(queryset=Widget.objects.all())

    class Meta:
        model = DeviceEntity
        fields = ["id", "name", "url", "config", "unit", "enabled", "widget_type", "entity_type_id", "widget_id"]
