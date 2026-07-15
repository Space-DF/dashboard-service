from common.pagination.base_pagination import BasePagination
from common.views.space import (
    SpaceListCreateAPIView,
    SpaceRetrieveUpdateDestroyAPIView,
    SpaceUpdateAPIView,
)
from django.db import transaction
from common.apps.billing.mixins import QuotaMixin
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.dashboard.models import Dashboard, Widget
from apps.dashboard.quotas import DashboardQuota
from apps.dashboard.serializers import (
    DashboardSerializer,
    UpdateWidgetSerializer,
    WidgetSerializer,
)


class ListCreateDashboardView(QuotaMixin, SpaceListCreateAPIView):
    model = Dashboard
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()
    space_field = "space"
    pagination_class = BasePagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ["created_at"]
    search_fields = ["name"]
    quota_classes = [DashboardQuota]


class UpdateDeleteDashboardView(QuotaMixin, SpaceRetrieveUpdateDestroyAPIView):
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


class BulkUpdateWidgetView(SpaceUpdateAPIView):
    serializer_class = UpdateWidgetSerializer
    queryset = Widget.objects.all()
    space_field = "dashboard__space"
    http_method_names = ["put"]

    @swagger_auto_schema(
        request_body=UpdateWidgetSerializer(many=True),
        responses={200: UpdateWidgetSerializer(many=True)},
    )
    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = [data["id"] for data in serializer.validated_data]
        queryset = self.filter_queryset(self.get_queryset()).filter(id__in=ids)
        by_id = {value.id: value for value in queryset}
        instances = [by_id[id] for id in ids]

        serializer = self.get_serializer(
            instances, data=serializer.validated_data, many=True
        )
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()

        return Response(serializer.data, status=200)


class BulkCreateWidgetView(SpaceListCreateAPIView):
    model = Widget
    serializer_class = WidgetSerializer
    queryset = Widget.objects.all()
    space_field = "dashboard__space"
    http_method_names = ["post"]

    @swagger_auto_schema(
        request_body=WidgetSerializer(many=True),
        responses={201: WidgetSerializer(many=True)},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
        return Response(serializer.data, status=201)
