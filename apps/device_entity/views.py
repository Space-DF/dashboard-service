from common.pagination.base_pagination import BasePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from apps.device_entity.models import DeviceEntity, EntityType
from apps.device_entity.serializers import (
    DeviceEntitiesSerializer,
    DeviceEntityTypeSerializer,
)


class ListDeviceEntityTypesView(generics.ListAPIView):
    queryset = EntityType.objects.all()
    serializer_class = DeviceEntityTypeSerializer


class ListDeviceEntitiesView(generics.ListAPIView):
    queryset = DeviceEntity.objects.all()
    serializer_class = DeviceEntitiesSerializer
    pagination_class = BasePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("entity_type_id",)  # I think here it should be type name
    ordering_fields = ("name", "widget_type")
