from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from apps.dashboard.contants import WidgetPeriod


def validate_widget_configuration(configuration):
    start_time = configuration.get("start_time")
    end_time = configuration.get("end_time")
    period = configuration.get("period")

    has_time_range = bool(start_time) or bool(end_time)
    has_period = bool(period)

    if has_time_range and has_period:
        raise serializers.ValidationError(
            "Cannot provide both start_time/end_time and period"
        )

    if has_time_range:
        if not (bool(start_time) and bool(end_time)):
            raise serializers.ValidationError(
                "Both start_time and end_time must be provided together"
            )
    elif not has_period:
        raise serializers.ValidationError(
            "Must provide either start_time/end_time or period"
        )


def calculate_time_range(configuration):
    start_time = configuration.get("start_time")
    end_time = configuration.get("end_time")

    if start_time and end_time:
        return start_time, end_time

    period = configuration.get("period")
    now = timezone.now()

    if period == WidgetPeriod.HOUR:
        start = now - timedelta(hours=1)
    elif period == WidgetPeriod.DAY:
        start = now - timedelta(days=1)
    elif period == WidgetPeriod.WEEK:
        start = now - timedelta(weeks=1)
    else:
        start = now - timedelta(days=30)

    return start.isoformat(), now.isoformat()
