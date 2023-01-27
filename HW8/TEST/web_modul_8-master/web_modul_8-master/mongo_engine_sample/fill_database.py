import json
from datetime import datetime
from random import choice

from models import Author, Quote

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

def insert_authors(filename):
    Author.drop_collection()
    
    data: dict = load_json(filename)

    for author in data:
        new_author = Author(fullname=author['fullname'])
        new_author.born_date = datetime.strptime(author['born_date'], "%B %d, %Y").date()
        new_author.born_location = author['born_location']
        new_author.description = author['description']
        new_author.save()

def insert_quotes(filename):
    Quote.drop_collection()
    authors = Author.objects()
    data: dict = load_json(filename)

    for quote in data:
        new_quote = Quote(tags=quote['tags'])
        new_quote.author = choice(authors).id
        new_quote.quote = quote['quote']
        new_quote.save()


if __name__ == '__main__':
    insert_authors(r'json_data\authors.json')
    insert_quotes(r'json_data\quotes.json')