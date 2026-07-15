from common.apps.billing.mixins import BaseQuota


class DashboardQuota(BaseQuota):
    reserve_actions = {"create", "destroy"}
    rules = {
        "create": "dashboard.max_count",
        "destroy": "dashboard.max_count",
    }
