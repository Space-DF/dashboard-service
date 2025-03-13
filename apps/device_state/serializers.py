from rest_framework import serializers

from apps.device_state.models import (
    DailyDeviceState,
    HourlyDeviceState,
    MinutelyDeviceState,
    MonthlyDeviceState,
)


class MinutelyDeviceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinutelyDeviceState
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class HourlyDeviceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyDeviceState
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class DailyDeviceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyDeviceState
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class MonthlyDeviceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyDeviceState
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
