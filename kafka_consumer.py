from confluent_kafka import Consumer, KafkaError, KafkaException, Producer
import json
from datetime import datetime
from collections import defaultdict

# Initialize a dictionary to keep track of message counts per locale
message_counts = defaultdict(int)

def consume_messages():
    conf = {
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)

    consumer.subscribe(['user-login'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            message = json.loads(msg.value().decode('utf-8'))
            process_message(message)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def process_message(message):
    # Filter messages to only process those from "android" devices
    if message.get("device_type") != "android":
        return

    # Transform timestamp from UNIX to human-readable format
    timestamp = int(message["timestamp"])
    message["timestamp"] = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    # Increment the message count for the locale
    locale = message.get("locale", "unknown")
    message_counts[locale] += 1

    # Print the processed message and current count for the locale
    print(f"Processing message: {message}")
    print(f"Current count for locale {locale}: {message_counts[locale]}")

    # Produce the processed message to a new Kafka topic
    produce_message(message)

def produce_message(processed_message):
    conf = {'bootstrap.servers': 'localhost:29092'}
    producer = Producer(conf)
    producer.produce('processed-data-topic', json.dumps(processed_message).encode('utf-8'))
    producer.flush()

if __name__ == '__main__':
    consume_messages()
