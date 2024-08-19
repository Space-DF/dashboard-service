from device_state.views import (
    ListDailyDeviceStateView,
    ListHourlyDeviceStateView,
    ListMinutelyDeviceStateView,
    ListMonthlyDeviceStateView,
)
from django.urls import path

app_name = "device_state"

urlpatterns = [
    path(
        "device-states/minutely",
        ListMinutelyDeviceStateView.as_view(),
    ),
    path(
        "device-states/hourly",
        ListHourlyDeviceStateView.as_view(),
    ),
    path(
        "device-states/daily",
        ListDailyDeviceStateView.as_view(),
    ),
    path(
        "device-states/monthly",
        ListMonthlyDeviceStateView.as_view(),
    ),
]
