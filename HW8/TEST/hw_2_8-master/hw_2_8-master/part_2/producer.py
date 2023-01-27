from random import randint

import pika
import faker

from model_contact import Contacts


fake = faker.Faker()


def create_data_to_db():
    for _ in range(30):
        record = Contacts(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            sending=False,
            email_priority=bool(randint(0, 1))
        )
        record.save()


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_mailing_list')
    channel.queue_declare(queue='email_mailing_list')

    contacts = Contacts.objects()
    for contact in contacts:
        if contact.email_priority:
            channel.basic_publish(exchange='', routing_key='email_mailing_list', body=f'{contact.id}'.encode())
            contact.update(sending=True)
        else:
            channel.basic_publish(exchange='', routing_key='sms_mailing_list', body=f'{contact.id}'.encode())
            contact.update(sending=True)

    connection.close()


if __name__ == '__main__':
    create_data_to_db()
    main()
