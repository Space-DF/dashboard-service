from datetime import datetime, time, timedelta

from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework import serializers

from apps.dashboard.constants import DisplayType, WidgetPeriod


def _normalize_boundary_time(value, *, is_end: bool = False):
    parsed_date = parse_date(value)
    if parsed_date:
        boundary = time(23, 59, 59, 999999) if is_end else time(0, 0, 0)
        dt = datetime.combine(parsed_date, boundary)
        return timezone.make_aware(dt)

    parsed_datetime = parse_datetime(value)
    if parsed_datetime:
        return parsed_datetime

    raise serializers.ValidationError(f"Invalid datetime format: {value}")


def validate_widget_configuration(display_type, configuration):
    series_types = [
        DisplayType.CHART_TYPE,
        DisplayType.HISTOGRAM_TYPE,
    ]
    if display_type in series_types:
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
        start = _normalize_boundary_time(start_time)
        end = _normalize_boundary_time(end_time, is_end=True)
        return start.isoformat(), end.isoformat()

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
