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
        dashboards = Dashboard.objects.filter(is_deactivated=False).order_by(
            "created_at"
        )

        excess_ids = list(dashboards.values_list("id", flat=True)[max_dashboards:])
        count = (
            Dashboard.objects.filter(id__in=excess_ids).update(is_deactivated=True)
            if excess_ids
            else 0
        )
        if count:
            logger.info(
                "Downgrade: deactivated %s excess dashboards for org %s "
                "(kept %s active out of %s total).",
                count,
                org_slug,
                min(dashboards.count(), max_dashboards),
                dashboards.count(),
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
