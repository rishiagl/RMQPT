import os
import sys
import pika

# Create a global channel variable to hold our channel object in
channel = None
exchange_name = None
x = 0
y = 0
z = 0
i = 0
# Step #2
def on_open(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_open_callback=on_channel_open)

def on_channel_open(new_channel):
    global channel
    global exchange_name
    channel = new_channel
    channel.queue_declare(queue="", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

def on_queue_declared(frame):
    queue_name = frame.method.queue
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='ACCELEROMETER.0')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='ACCELEROMETER.1')
    channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key='ACCELEROMETER.2')

    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(
    queue=queue_name, on_message_callback=handle_delivery, auto_ack=True)


# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    global i, x, y, z
    if method.routing_key == 'ACCELEROMETER.0':
        x = body.decode()
    if method.routing_key == 'ACCELEROMETER.1':
        y = body.decode()
    if method.routing_key == 'ACCELEROMETER.2':
        z = body.decode()
    i = i + 1
    print(f" [{i}]: {x}, {y}, {z}")

# Closing
def on_close(connection, exception):
    # Invoked when the connection is closed
    connection.ioloop.stop()

# Step #1: Connect to RabbitMQ using the default parameters
credentials = pika.PlainCredentials('rishiagl', '1234')
parameters = pika.ConnectionParameters('52.66.250.239', 5672, 'vh1', credentials)
connection = pika.SelectConnection(parameters=parameters, on_open_callback=on_open, on_close_callback=on_close)

try:
    # Loop so we can communicate with RabbitMQ
    if len(sys.argv) < 2:
        print("Please Exchange Name")
        sys.exit(0)
    exchange_name = sys.argv[1]
    connection.ioloop.start()
    
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed.
    # The on_close callback is required to stop the io loop
    connection.ioloop.start()