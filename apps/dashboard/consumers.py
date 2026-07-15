"""Dashboard downgrade deactivation logic."""

import logging

from django_tenants.utils import schema_context

from apps.dashboard.models import Dashboard

logger = logging.getLogger(__name__)


def deactivate_excess_dashboards(
    organization_slug: str, limits: dict = None
) -> int:
    limits = limits or {}
    max_dashboards = limits.get("dashboard.max_count", 1)

    with schema_context(organization_slug):
        dashboards = Dashboard.objects.filter(
            is_deactivated=False
        ).order_by("created_at")

        excess_ids = list(
            dashboards.values_list("id", flat=True)[max_dashboards:]
        )
        count = (
            Dashboard.objects.filter(id__in=excess_ids).update(
                is_deactivated=True
            )
            if excess_ids
            else 0
        )
        if count:
            logger.info(
                "Downgrade: deactivated %s excess dashboards for org %s "
                "(kept %s active out of %s total).",
                count,
                organization_slug,
                min(len(dashboards), max_dashboards),
                len(dashboards),
            )
        return count
