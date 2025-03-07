from common.pagination.base_pagination import BasePagination
from common.views.space import SpaceListCreateAPIView, SpaceRetrieveUpdateDestroyAPIView
from apps.dashboard.models import Dashboard, Widget
from apps.dashboard.serializers import DashboardSerializer, WidgetSerializer
from rest_framework.filters import OrderingFilter, SearchFilter


class ListCreateDashboardView(SpaceListCreateAPIView):
    model = Dashboard
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()
    space_field = "space"
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


class ListCreateWidgetView(SpaceListCreateAPIView):
    model = Widget
    serializer_class = WidgetSerializer
    queryset = Widget.objects.all()
    space_field = "dashboard__space"
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

    def get_queryset(self):
        queryset = super().get_queryset()

        dashboard_id = self.kwargs["dashboard_id"]
        return queryset.filter(dashboard__id=dashboard_id)
