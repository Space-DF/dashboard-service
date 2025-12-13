from rest_framework import serializers

from apps.dashboard.contants import DisplayType


def validate_widget_configuration(display_type, configuration):
    series_types = [
        DisplayType.CHART_TYPE,
        DisplayType.TABLE_TYPE,
        DisplayType.HISTOGRAM_TYPE,
    ]

    if display_type in series_types:
        required_fields = ["start_time", "end_time", "group_by"]
        missing_fields = [
            field for field in required_fields if not configuration.get(field)
        ]

        if missing_fields:
            raise serializers.ValidationError(
                f"Type {display_type}' requires the following fields in configuration: {', '.join(missing_fields)}"
            )
