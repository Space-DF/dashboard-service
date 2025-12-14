from django.db import models


class DisplayType(models.TextChoices):
    GAUGE_TYPE = "gauge"
    CHART_TYPE = "chart"
    MAP_TYPE = "map"
    SLIDER_TYPE = "slider"
    SWITCH_TYPE = "switch"
    VALUE_TYPE = "value"
    HISTOGRAM_TYPE = "histogram"
    TABLE_TYPE = "table"

class WidgetPeriod(models.TextChoices):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"