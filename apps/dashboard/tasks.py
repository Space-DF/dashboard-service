import logging

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
    return deactivate_excess_dashboards(kwargs["org_slug"], kwargs.get("limits"))


@task(
    name="spacedf.tasks.dashboard_upgrade",
    autoretry_for=(Exception,),
    retry_backoff=2,
    max_retries=3,
)
def dashboard_upgrade_task(**kwargs):
    return reactivate_dashboards(kwargs["org_slug"])


def deactivate_excess_dashboards(organization_slug: str, limits: dict = None) -> int:
    limits = limits or {}
    max_dashboards = limits.get("dashboard.max_count")
    if max_dashboards is None:
        logger.warning(
            "Skipping dashboard deactivation for %s: dashboard.max_count not in event",
            organization_slug,
        )
        return 0

    with schema_context(organization_slug):
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
                organization_slug,
                min(len(dashboards), max_dashboards),
                len(dashboards),
            )
        return count


def reactivate_dashboards(organization_slug: str) -> int:
    """
    Reactivate dashboards that were deactivated during a prior downgrade.
    """
    with schema_context(organization_slug):
        count = Dashboard.objects.filter(is_deactivated=True).update(
            is_deactivated=False
        )
        if count:
            logger.info(
                "Renewal: reactivated %s dashboards for org %s.",
                count,
                organization_slug,
            )
        return count
