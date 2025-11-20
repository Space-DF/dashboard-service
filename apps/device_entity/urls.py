from django.urls import path

from apps.device_entity.views import (
  ListDeviceEntityTypesView
)

app_name = "device_entity"

urlpatterns = [
    path(
        "device-entity",
        ListDeviceEntityTypesView.as_view(),
    ),
]
