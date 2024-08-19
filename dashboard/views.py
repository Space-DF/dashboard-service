from common.apps.space_role.constants import SpacePermission
from common.pagination.base_pagination import BasePagination
from common.permissions.constants import DELETE_METHOD, POST_METHOD, UPDATE_METHODS
from common.permissions.permission_classes import has_space_permission_access, is_method
from common.permissions.permission_condition import PermissionCondition
from common.views.space import SpaceListCreateAPIView, SpaceRetrieveUpdateDestroyAPIView
from dashboard.models import Dashboard, Widget
from dashboard.serializers import DashboardSerializer, WidgetSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class ListCreateDashboardView(SpaceListCreateAPIView):
    model = Dashboard
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()
    space_field = "space"
    permission_classes = [
        IsAuthenticated,
        PermissionCondition.Or(
            PermissionCondition.And(
                is_method(SAFE_METHODS),
                has_space_permission_access(SpacePermission.READ_DASHBOARD),
            ),
            PermissionCondition.And(
                is_method(POST_METHOD),
                has_space_permission_access(SpacePermission.CREATE_DASHBOARD),
            ),
        ),
    ]
    pagination_class = BasePagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["created_at"]
    search_fields = ["name"]


class UpdateDeleteDashboardView(SpaceRetrieveUpdateDestroyAPIView):
    model = Dashboard
    serializer_class = DashboardSerializer
    lookup_field = "id"
    queryset = Dashboard.objects.all()
    space_field = "space"
    permission_classes = [
        IsAuthenticated,
        PermissionCondition.Or(
            PermissionCondition.And(
                is_method(SAFE_METHODS),
                has_space_permission_access(SpacePermission.READ_DASHBOARD),
            ),
            PermissionCondition.And(
                is_method(UPDATE_METHODS),
                has_space_permission_access(SpacePermission.UPDATE_DASHBOARD),
            ),
            PermissionCondition.And(
                is_method(DELETE_METHOD),
                has_space_permission_access(SpacePermission.DELETE_DASHBOARD),
            ),
        ),
    ]


class ListCreateWidgetView(SpaceListCreateAPIView):
    model = Widget
    serializer_class = WidgetSerializer
    queryset = Widget.objects.all()
    space_field = "dashboard__space"
    permission_classes = [
        IsAuthenticated,
        PermissionCondition.Or(
            PermissionCondition.And(
                is_method(SAFE_METHODS),
                has_space_permission_access(SpacePermission.READ_DASHBOARD),
            ),
            PermissionCondition.And(
                is_method(POST_METHOD),
                has_space_permission_access(SpacePermission.UPDATE_DASHBOARD),
            ),
        ),
    ]
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        dashboard_id = self.kwargs["dashboard_id"]
        return queryset.filter(dashboard__id=dashboard_id)


class UpdateDeleteWidgetView(SpaceRetrieveUpdateDestroyAPIView):
    model = Widget
    serializer_class = WidgetSerializer
    lookup_field = "id"
    queryset = Widget.objects.all()
    space_field = "dashboard__space"
    permission_classes = [
        IsAuthenticated,
        PermissionCondition.Or(
            PermissionCondition.And(
                is_method(SAFE_METHODS),
                has_space_permission_access(SpacePermission.READ_DASHBOARD),
            ),
            PermissionCondition.And(
                is_method(UPDATE_METHODS),
                has_space_permission_access(SpacePermission.UPDATE_DASHBOARD),
            ),
            PermissionCondition.And(
                is_method(DELETE_METHOD),
                has_space_permission_access(SpacePermission.UPDATE_DASHBOARD),
            ),
        ),
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        dashboard_id = self.kwargs["dashboard_id"]
        return queryset.filter(dashboard__id=dashboard_id)
