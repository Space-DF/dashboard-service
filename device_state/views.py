from common.apps.space_role.constants import SpacePermission
from common.pagination.base_pagination import BasePagination
from common.permissions.permission_classes import has_space_permission_access
from common.views.space import SpaceListAPIView
from device_state.models import (
    DailyDeviceState,
    HourlyDeviceState,
    MinutelyDeviceState,
    MonthlyDeviceState,
)
from device_state.serializers import (
    DailyDeviceStateSerializer,
    HourlyDeviceStateSerializer,
    MinutelyDeviceStateSerializer,
    MonthlyDeviceStateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated


class ListDeviceStateView(SpaceListAPIView):
    space_field = "space"
    permission_classes = [
        IsAuthenticated,
        has_space_permission_access(SpacePermission.READ_DEVICE_STATE),
    ]
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
