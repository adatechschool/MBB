# accounts\service\apps.py

"""Django app configuration for the accounts service."""

import os
from django.apps import AppConfig
from accounts.service.infrastructure.kafka_consumer import start_consumer_thread


class AccountsServiceConfig(AppConfig):
    """Configuration class for the accounts service."""

    name = "accounts.service"
    label = "accounts_service"

    def ready(self):
        """Start the accounts service consumer thread."""
        if os.environ.get("RUN_MAIN") != "true":
            return
        start_consumer_thread()
