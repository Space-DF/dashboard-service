import logging

from common.apps.billing.constants import FeatureCode
from common.celery.tasks import task
from django_tenants.utils import schema_context

from apps.dashboard.models import Dashboard

logger = logging.getLogger(__name__)


@task(
    name="spacedf.tasks.dashboard_downgrade",
    autoretry_for=(Exception,),
    retry_backoff=2,
    max_retries=3,
)
def dashboard_downgrade_task(**kwargs):
    org_slug = kwargs["org_slug"]
    limits = kwargs.get("limits") or {}
    max_dashboards = limits.get(FeatureCode.DASHBOARD_MAX_COUNT)
    if max_dashboards is None:
        logger.warning(
            "Skipping dashboard deactivation for %s: %s not in event",
            org_slug,
            FeatureCode.DASHBOARD_MAX_COUNT,
        )
        return 0

    with schema_context(org_slug):
        # 1. fetch all active dashboards ordered by space, then created_at
        # 2. one bulk update of the collected excess ids.
        rows = list(
            Dashboard.objects.filter(is_deactivated=False)
            .values_list("id", "space_id")
            .order_by("space_id", "created_at")
        )
        excess_ids = []
        seen_space = None
        space_count = 0
        for dashboard_id, space_id in rows:
            if space_id != seen_space:
                seen_space = space_id
                space_count = 0
            space_count += 1
            if space_count > max_dashboards:
                excess_ids.append(dashboard_id)

        count = (
            Dashboard.objects.filter(id__in=excess_ids).update(is_deactivated=True)
            if excess_ids
            else 0
        )
        if count:
            logger.info(
                "Downgrade: deactivated %s excess dashboards for org %s "
                "(space limit %s).",
                count,
                org_slug,
                max_dashboards,
            )
        return count


@task(
    name="spacedf.tasks.dashboard_upgrade",
    autoretry_for=(Exception,),
    retry_backoff=2,
    max_retries=3,
)
def dashboard_upgrade_task(**kwargs):
    org_slug = kwargs["org_slug"]
    with schema_context(org_slug):
        count = Dashboard.objects.filter(is_deactivated=True).update(
            is_deactivated=False
        )
        if count:
            logger.info(
                "Renewal: reactivated %s dashboards for org %s.",
                count,
                org_slug,
            )
        return count
