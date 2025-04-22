# accounts/service/infrastructure/kafka_consumer.py
import json
import threading
import time
from kafka import KafkaConsumer
from django.conf import settings
from common.models import User, Role

TOPIC = "user.created"
BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS  # e.g. ["broker1:9092"]


def process_message(message):
    payload = json.loads(message.value.decode("utf-8"))
    user_id = payload["user_id"]
    username = payload["username"]
    email = payload["email"]

    # idempotent insert: if already exists, skip
    if User.objects.filter(user_id=user_id).exists():
        return

    # assign default role (e.g. "user")
    default_role, _ = Role.objects.get_or_create(role_name="user")

    User.objects.create(
        user_id=user_id,
        username=username,
        email=email,
        role=default_role,
        password="",  # Auth service manages passwords
        is_active=True,
    )


def consumer_loop():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="accounts-service",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    for message in consumer:
        try:
            process_message(message)
        except Exception:
            # log & continue
            import logging
            logging.exception("Failed to process user.created message")


def start_consumer_thread():
    thread = threading.Thread(target=consumer_loop, daemon=True)
    thread.start()
