from common.models.base_model import BaseModel
from dashboard.models import Widget
from django.db import models


class EntityType(BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField()
    
class DeviceEntity(BaseModel):
    name = models.CharField(max_length=256)
    url = models.TextField()
    config = models.JSONField()
    unit = models.CharField(max_length=256)
    enabled = models.BooleanField(default=True)
    widget_type = models.CharField(max_length=256)
    entity_type_id = models.ForeignKey(EntityType, on_delete=models.CASCADE)
    widget_id = models.ForeignKey(Widget, on_delete=models.CASCADE)


