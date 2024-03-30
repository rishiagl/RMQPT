import pika
import sys

credentials = pika.PlainCredentials('rishiagl', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters('52.66.250.239', 5672, 'vh1', credentials))
channel_x = connection.channel()
channel_y = connection.channel()
channel_z = connection.channel()

if len(sys.argv) < 2:
    print("Please Exchange Name")
    sys.exit(0)
exchange_name = sys.argv[1]

result_x = channel_x.queue_declare('', exclusive=True)
result_y = channel_y.queue_declare('', exclusive=True)
result_z = channel_z.queue_declare('', exclusive=True)

queue_x = result_x.method.queue
queue_y = result_y.method.queue
queue_z = result_z.method.queue

channel_x.queue_bind(
        exchange=exchange_name, queue=queue_x, routing_key="ACCELEROMETER.0")
channel_y.queue_bind(
        exchange=exchange_name, queue=queue_y, routing_key="ACCELEROMETER.1")
channel_z.queue_bind(
        exchange=exchange_name, queue=queue_z, routing_key="ACCELEROMETER.2")

print(' [*] Waiting for logs. To exit press CTRL+C')

cur_x = 0
cur_y = 0
cur_z = 0

def callback_x(ch, method, properties, body):
    global cur_x
    cur_x = body
    display()

def callback_y(ch, method, properties, body):
    global cur_y
    cur_y = body

def callback_z(ch, method, properties, body):
    global cur_z
    cur_z = body


def display():
    print(f" [x]: {cur_x}, {cur_y}, {cur_z}")


channel_x.basic_consume(
    queue=queue_x, on_message_callback=callback_x, auto_ack=True)
channel_y.basic_consume(
    queue=queue_y, on_message_callback=callback_y, auto_ack=True)
channel_z.basic_consume(
    queue=queue_z, on_message_callback=callback_z, auto_ack=True)

channel_x.start_consuming()
channel_y.start_consuming()
channel_z.start_consuming()