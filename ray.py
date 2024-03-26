import pika
import sys

credentials = pika.PlainCredentials('rishiagl', '1234')
connection = pika.BlockingConnection(pika.ConnectionParameters('52.66.250.239', 5672, 'vh1', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='mobile', exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange='mobile', queue=queue_name, routing_key="acc.1")

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()