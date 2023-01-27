from random import randint

from faker import Faker

from models import Contact

def generate_contacts(contactCount:int):
    Contact.drop_collection()

    faker = Faker()
    generated_contacts = []

    for _ in range(contactCount):
        new_contact = Contact(fullname=faker.name())
        new_contact.age = randint(16, 80)
        new_contact.email = faker.email()
        new_contact.phoneNumber = faker.phone_number()
        new_contact.country = faker.country()
        new_contact.save()

        generated_contacts.append(new_contact)

    return generated_contacts

def get_contact_ids(contacts: list[Contact]):
    return [contact.id for contact in contacts]
