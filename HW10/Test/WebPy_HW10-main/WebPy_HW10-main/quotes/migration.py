import psycopg2
import pymongo
import configparser

config = configparser.ConfigParser()
config.read('src/config.ini')  # to read the config file


# Connect to MongoDB and retrieve data: mongodb+srv://goitlearn:Seoul@cluster0.aksl02l.mongodb.net/test
def mongo() -> None:
    m_user = config.get('mongo', 'user')
    m_pass = config.get('mongo', 'pass')
    db_name = config.get('mongo', 'db_name')
    domain = config.get('mongo', 'domain')

    connect(host = f"mongodb+srv://{m_user}:{m_pass}@{domain}/{db_name}?retryWrites=true&w=majority")
    client = pymongo.MongoClient(connect)

    db = client["postgres"]
    collection = db["mycollection"]
    data = collection.find()

# Connect to PostgreSQL and create the appropriate models
conn = psycopg2.connect(
    host="127.0.0.1",
    database="postgres",
    user="postgres",
    password="Seoul"
)
cursor = conn.cursor()

# Iterate over the data in MongoDB and create records in PostgreSQL = TBC
for item in data:
    cursor.execute(
        "INSERT INTO mytable (field1, field2, field3) "
        "VALUES (%s, %s, %s)",
        (item["field1"], item["field2"], item["field3"])
    )

# Commit the changes and close the connection
conn.commit()
conn.close()
