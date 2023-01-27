import configparser
from pymongo import MongoClient


config = configparser.ConfigParser()

config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')

connection_string = f"mongodb+srv://{mongo_user}:{mongodb_pass}@modul8claster.vr5vme3.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
