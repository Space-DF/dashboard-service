import logging

from common.apps.billing.constants import FeatureCode
from common.celery.tasks import PermanentTaskError, task
from django_tenants.utils import schema_context

from apps.dashboard.models import Dashboard

logger = logging.getLogger(__name__)


def _is_unlimited(kwargs, feature_code):
    return feature_code in set(kwargs.get("unlimited_features") or [])


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
        raise PermanentTaskError(
            "dashboard downgrade requires limit %s for org %s"
            % (FeatureCode.DASHBOARD_MAX_COUNT, org_slug)
        )
    if max_dashboards < 0:
        raise PermanentTaskError(
            "dashboard downgrade limit %s must be >= 0 for org %s"
            % (FeatureCode.DASHBOARD_MAX_COUNT, org_slug)
        )

    downgraded_at = kwargs.get("downgraded_at")

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
            Dashboard.objects.filter(id__in=excess_ids).update(
                is_deactivated=True, deactivated_at=downgraded_at
            )
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
    limits = kwargs.get("limits") or {}
    max_dashboards = limits.get(FeatureCode.DASHBOARD_MAX_COUNT)
    unlimited_dashboards = _is_unlimited(kwargs, FeatureCode.DASHBOARD_MAX_COUNT)
    if max_dashboards is None and not unlimited_dashboards:
        raise PermanentTaskError(
            "dashboard upgrade requires limit or explicit unlimited feature %s for org %s"
            % (FeatureCode.DASHBOARD_MAX_COUNT, org_slug)
        )
    if max_dashboards is not None and max_dashboards < 0:
        raise PermanentTaskError(
            "dashboard upgrade limit %s must be >= 0 for org %s"
            % (FeatureCode.DASHBOARD_MAX_COUNT, org_slug)
        )

    with schema_context(org_slug):
        if max_dashboards is None:
            count = Dashboard.objects.filter(is_deactivated=True).update(
                is_deactivated=False, deactivated_at=None
            )
        else:
            active_counts = {}
            for dashboard_id, space_id in (
                Dashboard.objects.filter(is_deactivated=False)
                .values_list("id", "space_id")
                .order_by("space_id", "created_at")
            ):
                active_counts[space_id] = active_counts.get(space_id, 0) + 1

            reactivated_ids = []
            for dashboard_id, space_id in (
                Dashboard.objects.filter(is_deactivated=True)
                .values_list("id", "space_id")
                .order_by("space_id", "created_at")
            ):
                space_active_count = active_counts.get(space_id, 0)
                if space_active_count >= max_dashboards:
                    continue
                reactivated_ids.append(dashboard_id)
                active_counts[space_id] = space_active_count + 1

            count = (
                Dashboard.objects.filter(id__in=reactivated_ids).update(
                    is_deactivated=False, deactivated_at=None
                )
                if reactivated_ids
                else 0
            )
        if count:
            logger.info(
                "Renewal: reactivated %s dashboards for org %s.",
                count,
                org_slug,
            )
        return count
