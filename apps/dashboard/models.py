from common.apps.space.models import Space
from common.models.base_model import BaseModel
from django.db import models


class Dashboard(BaseModel):
    name = models.CharField(max_length=256)
    space = models.ForeignKey(Space, related_name="dashboard", on_delete=models.CASCADE)


class Widget(BaseModel):
    configuration = models.JSONField()
    dashboard = models.ForeignKey(
        Dashboard, related_name="widget", on_delete=models.CASCADE
    )
