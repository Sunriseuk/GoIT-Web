import pickle
import pika


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='connect_queue', durable=True)

def callback(ch, method, properties, body):
    message = pickle.loads(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    def message_sender():
        print(message.email)
    return message_sender()


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='connect_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
