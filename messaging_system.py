import pika
import json
import argparse

# RabbitMQ Connection Parameters
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'task_queue'
EXCHANGE_NAME = 'logs'


def send_p2p_message():
    """Send a Point-to-Point (P2P) message"""
    order_id = input("Enter order ID: ")
    customer = input("Enter customer name: ")

    message = {
        "type": "order",
        "orderId": order_id,
        "customer": customer
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(message))
    print(f"[x] Sent P2P Message: {message}")
    connection.close()


def receive_p2p_message():
    """Receive a P2P message"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"[x] Received P2P Message: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def publish_message():
    """Publish a message in the Pub-Sub model"""
    event = input("Enter event type: ")
    product = input("Enter product name: ")
    price = input("Enter product price: ")

    message = {
        "event": event,
        "product": product,
        "price": price
    }
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key='', body=json.dumps(message))
    print(f"[x] Published Message: {message}")
    connection.close()


def subscribe_messages():
    """Subscribe to messages in the Pub-Sub model"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"[x] Received Pub-Sub Message: {message}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def main():
    parser = argparse.ArgumentParser(description="Messaging System CLI")
    parser.add_argument("action", choices=["send_p2p", "receive_p2p", "publish", "subscribe"], help="Choose an action")
    args = parser.parse_args()

    if args.action == "send_p2p":
        send_p2p_message()
    elif args.action == "receive_p2p":
        receive_p2p_message()
    elif args.action == "publish":
        publish_message()
    elif args.action == "subscribe":
        subscribe_messages()


if __name__ == "__main__":
    main()
