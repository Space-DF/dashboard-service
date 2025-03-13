from common.apps.space.models import Space
from common.models.base_model import BaseModel
from django.db import models


class DeviceState(BaseModel):
    state_name = models.CharField(max_length=256)
    device_slug_name = models.SlugField(max_length=256)
    value = models.DecimalField(max_digits=19, decimal_places=10)
    from_timestamp = models.DateTimeField()
    space = models.ForeignKey(Space, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MinutelyDeviceState(DeviceState):
    pass


class HourlyDeviceState(DeviceState):
    pass


class DailyDeviceState(DeviceState):
    pass


class MonthlyDeviceState(DeviceState):
    pass
