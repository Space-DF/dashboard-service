from common.pagination.base_pagination import BasePagination
from common.views.space import SpaceListAPIView
from apps.device_state.models import (
    DailyDeviceState,
    HourlyDeviceState,
    MinutelyDeviceState,
    MonthlyDeviceState,
)
from apps.device_state.serializers import (
    DailyDeviceStateSerializer,
    HourlyDeviceStateSerializer,
    MinutelyDeviceStateSerializer,
    MonthlyDeviceStateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ListDeviceStateView(SpaceListAPIView):
    space_field = "space"
    pagination_class = BasePagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["from_timestamp"]
    filterset_fields = ["state_name", "device_slug_name"]


class ListMinutelyDeviceStateView(ListDeviceStateView):
    model = MinutelyDeviceState
    serializer_class = MinutelyDeviceStateSerializer
    queryset = MinutelyDeviceState.objects.all()


class ListHourlyDeviceStateView(ListDeviceStateView):
    model = HourlyDeviceState
    serializer_class = HourlyDeviceStateSerializer
    queryset = HourlyDeviceState.objects.all()


class ListDailyDeviceStateView(ListDeviceStateView):
    model = DailyDeviceState
    serializer_class = DailyDeviceStateSerializer
    queryset = DailyDeviceState.objects.all()


class ListMonthlyDeviceStateView(ListDeviceStateView):
    model = MonthlyDeviceState
    serializer_class = MonthlyDeviceStateSerializer
    queryset = MonthlyDeviceState.objects.all()
