# accounts\service\apps.py

"""Django app configuration for the accounts service."""

import os
from django.apps import AppConfig


class AccountsServiceConfig(AppConfig):
    """Configuration class for the accounts service."""

    name = "accounts.service"
    label = "accounts_service"

    def ready(self):
        """Start the accounts service consumer thread."""
        if os.environ.get("RUN_MAIN") != "true":
            return
        from accounts.service.infrastructure.kafka_consumer import start_consumer_thread

        start_consumer_thread()
