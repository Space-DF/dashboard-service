from common.apps.space.models import Space
from common.models.base_model import BaseModel
from django.db import models

from apps.dashboard.constants import DisplayType


class Dashboard(BaseModel):
    name = models.CharField(max_length=256)
    space = models.ForeignKey(Space, related_name="dashboard", on_delete=models.CASCADE)
    is_deactivated = models.BooleanField(default=False)


class Widget(BaseModel):
    dashboard = models.ForeignKey(
        Dashboard, related_name="dashboard_widgets", on_delete=models.CASCADE
    )
    display_type = models.CharField(
        max_length=256, choices=DisplayType.choices, default=DisplayType.GAUGE_TYPE
    )
    entity_id = models.CharField(max_length=256, null=True, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    configuration = models.JSONField(null=True, blank=True)
