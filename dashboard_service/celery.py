import importlib.util
import os
import sys

if importlib.util.find_spec("common") is None:
    sys.path.append(
        os.path.abspath(os.path.join("..", "django-common-utils"))
    )  # Import django-common-utils without install

from celery import Celery
from common.celery.routing import (
    setup_organization_task_routing,
    setup_subscription_task_routing,
    setup_synchronous_model_task_routing,
)
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard_service.settings")
app = Celery("dashboard_service")
app.config_from_object("django.conf:settings", namespace="CELERY")

setup_organization_task_routing()
setup_synchronous_model_task_routing()
setup_subscription_task_routing(["dashboard_downgrade", "dashboard_upgrade"])

app.autodiscover_tasks(settings.CELERY_TASKS)
