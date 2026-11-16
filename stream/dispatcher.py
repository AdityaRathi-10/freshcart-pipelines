"""Publish FreshCart-style orders to a RabbitMQ topic exchange."""

from __future__ import annotations

import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

import pika

EXCHANGE = "rapido-dispatch"
CITIES = {"bangalore": ["koramangala", "indiranagar", "whitefield"], "chennai": ["tnagar", "whitefield"]}
ORDER_TYPES = ("ride", "food")


def connection() -> pika.BlockingConnection:
    url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
    return pika.BlockingConnection(pika.URLParameters(url))


def publish(channel: pika.adapters.blocking_connection.BlockingChannel, bad: bool = False) -> dict:
    city = random.choice(list(CITIES))
    zone = random.choice(CITIES[city])
    order_type = random.choice(ORDER_TYPES)
    message = {
        "id": str(uuid.uuid4()),
        "city": city,
        "zone": zone,
        "type": order_type,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    if bad:
        message.pop("zone")
    key = f"{city}.{zone}.{order_type}" if "zone" in message else f"{city}.unknown.{order_type}"
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=key,
        body=json.dumps(message),
        properties=pika.BasicProperties(content_type="application/json", delivery_mode=2),
    )
    return message


def main() -> None:
    with connection() as conn:
        channel = conn.channel()
        channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
        count = 0
        while True:
            count += 1
            message = publish(channel, bad=count % 10 == 0)
            print(f"published id={message['id']} payload={message}", flush=True)
            time.sleep(2)


if __name__ == "__main__":
    main()

