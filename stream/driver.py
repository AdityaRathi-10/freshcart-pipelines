"""Consume dispatcher messages using a private topic-bound queue."""

from __future__ import annotations

import argparse
import json
import os

import pika

EXCHANGE = "rapido-dispatch"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("pattern")
    args = parser.parse_args()
    url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    queue = channel.queue_declare(queue="", exclusive=True, auto_delete=True).method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=args.pattern)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body)
            if not message.get("zone"):
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                print(f"{args.name}: NACK dropped id={message.get('id')}", flush=True)
                return
            print(f"{args.name}: processed key={method.routing_key} message={message}", flush=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except (json.JSONDecodeError, TypeError, KeyError) as exc:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            print(f"{args.name}: NACK malformed message ({exc})", flush=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    print(f"{args.name}: listening on {args.pattern}", flush=True)
    try:
        channel.start_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()

