from common.apps.billing.constants import FeatureCode, FeatureUsageScope
from common.apps.billing.mixins import BaseQuota


class DashboardQuota(BaseQuota):
    reserve_actions = {"create"}
    release_actions = {"destroy"}
    rules = {
        "create": {
            "feature": FeatureCode.DASHBOARD_MAX_COUNT,
            "scope": FeatureUsageScope.SPACE,
        },
        "destroy": {
            "feature": FeatureCode.DASHBOARD_MAX_COUNT,
            "scope": FeatureUsageScope.SPACE,
        },
    }
