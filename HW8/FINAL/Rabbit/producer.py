from models import Contact
import faker
import pika
from mongoengine import connect
import pickle


connect(host=f"mongodb+srv://mspryst:tq38bIkpcJGUCviq@cluster0.c5xjo1y.mongodb.net/myRabbitMq?retryWrites=true&w=majority", ssl=True)

fake_data = faker.Faker()
for _ in range(5):
    author = Contact(fullname=fake_data.name(), email=fake_data.email())
    author.save()

contacts = Contact.objects()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='connect_queue', durable=True)

def main():
    for contact in contacts:
        channel.basic_publish(exchange='', routing_key='connect_queue', body=pickle.dumps(contact))
        contact.update(done=True)
        print('The message was sent')

    connection.close()
    

if __name__ == '__main__':
    main()
    