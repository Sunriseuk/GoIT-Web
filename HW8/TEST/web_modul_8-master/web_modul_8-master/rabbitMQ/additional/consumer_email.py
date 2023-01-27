from time import sleep

import pika

from models import Contact

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue="send_by_email")

    def callback(ch, method, properties, body):
        contacts = Contact.objects()
        contact_id = body.decode()
        contact_email = contacts(id=contact_id)[0].email
        
        sleep(0.5)

        print(f" [x] Sent message to contact's email: '{contact_email}' with id: {contact_id}")

        contacts(id=contact_id)[0].update(sended=True)

    channel.basic_consume(queue='send_by_email', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for user identifiers. To exit press CTRL+C')
    
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping consuming...")
    