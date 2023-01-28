import json
from time import sleep
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credential=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback_result(ch, method, properties, body):
    message = json.loads(body)
    print(f'Received message: {message}')
    sleep(1)
    print('Done!')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='Hello', on_message_callback=callback_result)
channel.start_consuming()




# import pika
#
# def main():
#     credential = pika.PlainCredentials('guest', 'guest')
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credential=credential))
#     channel = connection.channel()
#
#     channel.queue_declare(queue='Hello')
#
#     def my_callback(ch, method, properties, body):
#         print(' [x] Received %r' % body)
#
#
#     channel.basic_consume(queue='Hello', on_message_callback=my_callback, auto_ack=True)
#     channel.start_consuming()
#
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print('Good Buy')