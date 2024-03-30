import pika
import sys

credentials = pika.PlainCredentials('rishiagl', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters('52.66.250.239', 5672, 'vh1', credentials))
channel = connection.channel()

if len(sys.argv) < 2:
    print("Please Exchange Name")
    sys.exit(0)
exchange_name = sys.argv[1]

if len(sys.argv) < 3:
    print("please provide routinge Key")
    sys.exit(1)
routing_key = sys.argv[2]

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=routing_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()