from apps.device_state.models import (
    DailyDeviceState,
    HourlyDeviceState,
    MinutelyDeviceState,
    MonthlyDeviceState,
)
from django.contrib import admin


class DeviceStateAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "state_name",
        "device_slug_name",
        "value",
        "from_timestamp",
        "space",
        "created_at",
        "updated_at",
    )


@admin.register(MinutelyDeviceState)
class MinutelyDeviceStateAdmin(DeviceStateAdmin):
    pass


@admin.register(HourlyDeviceState)
class HourlyDeviceStateAdmin(DeviceStateAdmin):
    pass


@admin.register(DailyDeviceState)
class DailyDeviceStateAdmin(DeviceStateAdmin):
    pass


@admin.register(MonthlyDeviceState)
class MonthlyDeviceStateAdmin(DeviceStateAdmin):
    pass
