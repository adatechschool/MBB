# common\events.py

"""Module for publishing events to Kafka topics."""

import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=["broker1:9092"])


def publish_event(topic: str, payload: dict):
    """Publish an event to a Kafka topic.

    Args:
        topic (str): The Kafka topic to publish to
        payload (dict): The event payload to be serialized and published
    """
    producer.send(topic, json.dumps(payload).encode("utf-8"))
    producer.flush()
