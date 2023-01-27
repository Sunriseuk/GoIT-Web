import redis
from redis_lru import RedisLRU

from models import Author, Quote


client = redis.StrictRedis(host="localhost", port=6379, password=None)
redis_cache = RedisLRU(client)

@redis_cache
def query_authors(value):
    authors = Author.objects
    return authors(fullname__istartswith=value)

@redis_cache
def query_quotes(value):
    quotes = Quote.objects
    return quotes(tags__contains=value)

def output_response(response):
    for record in response:
        print(record.to_json())
    
def query_db_cycle():
    while True:
        command: str = input("Enter query(command:values): ")

        if command.lower() == 'exit':
            break

        command, values = command.split(":")

        if command.lower() == "name":
            print(f"Author with name '{values}':")
            output_response(query_authors(values))

        elif command.lower() == "tag":
            if ',' in values:
                for value in values.split(','):
                    print(f"Quotes with tag '{value}':")
                    output_response(query_quotes(value))
            else:
                print(f"Quotes with tag '{values}':")
                output_response(query_quotes(values))
            
        
if __name__ == '__main__':
    query_db_cycle()
        