"""Run the dashboard downgrade consumer."""
from django.core.management.base import BaseCommand

from apps.dashboard.consumers import deactivate_excess_dashboards
from common.utils.downgrade_consumer import run_downgrade_consumer


class Command(BaseCommand):
    help = "Listen for org.downgraded events and deactivate excess dashboards."

    def handle(self, *args, **options):
        self.stdout.write("Starting dashboard downgrade consumer...")
        run_downgrade_consumer(
            queue_name="dashboard.org.events.queue",
            callback=deactivate_excess_dashboards,
        )
