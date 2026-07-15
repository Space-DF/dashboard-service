from common.apps.billing.mixins import BaseQuota


class DashboardQuota(BaseQuota):
    release_actions = {"destroy"}
    rules = {
        "create": "dashboard.max_count",
        "destroy": "dashboard.max_count",
    }
