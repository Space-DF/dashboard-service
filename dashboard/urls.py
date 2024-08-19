from dashboard.views import (
    ListCreateDashboardView,
    ListCreateWidgetView,
    UpdateDeleteDashboardView,
    UpdateDeleteWidgetView,
)
from django.urls import path

app_name = "dashboard"

urlpatterns = [
    path(
        "dashboards",
        ListCreateDashboardView.as_view(),
    ),
    path(
        "dashboards/<str:id>",
        UpdateDeleteDashboardView.as_view(),
    ),
    path(
        "dashboards/<str:dashboard_id>/widgets",
        ListCreateWidgetView.as_view(),
    ),
    path(
        "dashboards/<str:dashboard_id>/widgets/<str:id>",
        UpdateDeleteWidgetView.as_view(),
    ),
]
