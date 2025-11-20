from django.urls import path

from apps.device_entity.views import ListDeviceEntitiesView, ListDeviceEntityTypesView

app_name = "device_entity"

urlpatterns = [
    path("device-entity/types", ListDeviceEntityTypesView.as_view()),
    path("device-entity/entities", ListDeviceEntitiesView.as_view()),
]
