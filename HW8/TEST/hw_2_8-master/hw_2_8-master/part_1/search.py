from models import Quotes
import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def pars_input(query) -> dict:
    list_args = query.split(':')
    field = list_args[0]
    value = list_args[-1].strip().split(',')
    return {field: value}


@cache
def find_quotes_to_name(name):
    author_name = ''
    all_quotes = []
    quotes = Quotes.objects()
    for quote in quotes:
        if quote.author.fullname.capitalize() == name.capitalize(
        ) or quote.author.fullname.capitalize().startswith(name.capitalize()):
            author_name = quote.author.fullname
            all_quotes.append(quote.quote)
    return f'All quotes by {author_name}: {all_quotes}'


@cache
def find_quote_to_tag(tag_to_search):
    all_quotes = []
    quotes = Quotes.objects()
    for quote in quotes:
        for tag in quote.tags:
            if tag.startswith(tag_to_search):
                all_quotes.append(f'Quote by {quote.author.fullname} with tag {tag}: {quote.quote}')
    return all_quotes


search = True

while search:
    query = input("Ready to search... ")

    if query == "exit":
        search = False

    else:
        query_dict = pars_input(query)

        if 'name' in query_dict:
            for name in query_dict['name']:
                print(find_quotes_to_name(name))

        if 'tag' in query_dict:
            for el in query_dict['tag']:
                print(find_quote_to_tag(el))

        if 'tags' in query_dict:
            for el in query_dict['tags']:
                print(find_quote_to_tag(el))
