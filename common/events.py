# common\events.py

"""Module for publishing events to Kafka topics."""

import json
from kafka import KafkaProducer, errors

try:
    producer = KafkaProducer(
        bootstrap_servers=["broker1:9092"],
        linger_ms=500,
        batch_size=32768,
    )
except errors.NoBrokersAvailable:
    producer = None


def publish_event(topic: str, payload: dict):
    """Publish an event to a Kafka topic if broker is available.

    Args:
        topic (str): The Kafka topic to publish to
        payload (dict): The event payload to be serialized and published
    """
    if producer is None:
        # Broker unavailable; skip publishing gracefully
        return
    # Send asynchronously; flush handled by background tasks
    producer.send(topic, json.dumps(payload).encode("utf-8"))
