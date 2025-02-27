
# Messaging System with RabbitMQ

This project demonstrates a simple messaging system using **RabbitMQ** for message queuing. The system supports both **Point-to-Point (P2P)** messaging and **Publish-Subscribe (Pub-Sub)** messaging patterns.

## Prerequisites

- **Docker**: Make sure you have Docker installed on your machine to run RabbitMQ in a container.
- **Python**: This project uses Python 3.x. You need to have Python and the required dependencies installed.

## Getting Started

### Step 1: Set Up RabbitMQ Using Docker Compose

To start RabbitMQ, you can use Docker Compose. Follow these steps:

1. Clone this repository to your local machine.
2. In the project folder, run the following command to bring up the RabbitMQ container:

   ```bash
   docker-compose up
   ```

   This will start RabbitMQ on ports:
   - `5672`: RabbitMQ main port for communication.
   - `15672`: RabbitMQ Management UI (accessible through `http://localhost:15672`).

   The default RabbitMQ username is `guest` and the password is `guest`.

### Step 2: Install Python Dependencies

Make sure you have `pika` installed, which is the Python RabbitMQ client library. You can install it using `pip`:

```bash
pip install pika
```

### Step 3: Run the Messaging System

You can interact with the messaging system using the `messaging_system.py` script, which supports the following actions:

- **send_p2p**: Send a Point-to-Point (P2P) message to the queue.
- **receive_p2p**: Receive a P2P message from the queue.
- **publish**: Publish a message in the Publish-Subscribe (Pub-Sub) model.
- **subscribe**: Subscribe to messages in the Pub-Sub model.

### Available Commands

#### Send a P2P Message

To send a message in a point-to-point manner, use the following command:

```bash
python messaging_system.py send_p2p
```

It will prompt you to input the `order ID` and `customer name`, and then send the message to the `task_queue`.

#### Receive a P2P Message

To receive a P2P message from the queue, use this command:

```bash
python messaging_system.py receive_p2p
```

This will start consuming messages from the queue and print them as they are received.

#### Publish a Message

To publish a message in the Pub-Sub model, use this command:

```bash
python messaging_system.py publish
```

It will prompt you to input the `event type`, `product name`, and `price`, and then publish the message to the `logs` exchange.

#### Subscribe to Messages

To subscribe to messages published in the Pub-Sub model, use this command:

```bash
python messaging_system.py subscribe
```

This will start consuming messages from the `logs` exchange and print them as they are received by any subscribers.

### Program Workflow

1. **send_p2p_message**: The `send_p2p_message()` function allows you to send a point-to-point message. When you run this action, you'll be prompted to input the `order ID` and `customer name`. The message is then sent to the `task_queue` in RabbitMQ.
   
2. **receive_p2p_message**: The `receive_p2p_message()` function listens for and receives messages from the `task_queue`. It will keep running until you stop it manually. When a message is received, it prints the message contents.

3. **publish_message**: The `publish_message()` function sends a message to all subscribers using the Publish-Subscribe pattern. The message is sent to the `logs` exchange, and subscribers to this exchange will receive it.

4. **subscribe_messages**: The `subscribe_messages()` function listens for messages sent to the `logs` exchange. Any published messages will be printed by subscribers.

## RabbitMQ Management UI

You can monitor RabbitMQ and check queues, exchanges, and messages using the RabbitMQ Management UI at:

- **URL**: [http://localhost:15672](http://localhost:15672)
- **Username**: `guest`
- **Password**: `guest`

## Notes

- **Queue Durability**: In the point-to-point messaging (`send_p2p_message` and `receive_p2p_message`), the queue is durable, which means it will survive RabbitMQ restarts.
- **Exchange Type**: The `logs` exchange used in the publish-subscribe model is of type `fanout`, meaning it broadcasts messages to all queues bound to it.

## Conclusion

This simple messaging system demonstrates how you can work with RabbitMQ in Python for both point-to-point and publish-subscribe messaging patterns. Use it to build distributed systems or applications that require message-based communication.
