import pika

from models import Contact
from fill_db import get_contact_ids, get_contact_methods, generate_contacts

def main(contacts: list[Contact]):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue="send_by_email")
    channel.queue_declare(queue="send_by_phone")

    for id, by_email_method in zip(get_contact_ids(contacts), get_contact_methods(contacts)):
        if by_email_method:
            queue = "send_by_email"
        else:
            queue = "send_by_phone"

        channel.basic_publish(exchange='', routing_key=queue, body=str(id))
        
        print(f" [x] Sent id: {id}")

    connection.close()


if __name__ == '__main__':
    contacts = generate_contacts(20)
    main(contacts)
    