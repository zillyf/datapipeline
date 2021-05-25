# pip3 install kafka
from kafka import KafkaConsumer
from json import loads
from time import sleep
import os
import sys

# pip3 install pymongo
from pymongo import MongoClient

# wait for startup of Kafka
sys.stdout.write("wait for startup of Kafka\n")
sleep(15)

dbServer = os.getenv("MONGO_DB_SERVER", "localhost:27017")
dbUser = os.getenv("MONGO_USERNAME", "searchengine")
dbPW = os.getenv("MONGO_PASSWORD", "searchengine")

kafkaServer = os.getenv("KAFKA_SERVER", "localhost:9092")

client = MongoClient(dbServer, username=dbUser, password=dbPW)

sys.stdout.write("Mongo DB Connection -----\n")
sys.stdout.write("server:" + dbServer + "\n")
sys.stdout.write("user:" + dbUser + "\n")

collection = client.images.images

kafkaTopic = os.getenv("KAFKA_TOPIC_SENDFILES", "send_file")

print("Kafka Connection -----")
print("server:" + kafkaServer)
print("topic:" + kafkaTopic)


consumer = KafkaConsumer(
    kafkaTopic,
    bootstrap_servers=[kafkaServer],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group-id",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)

print("kafka init completed")

for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    # collection.insert_one(  event_data )
    if "filenameHash" in event_data:
        key = {"filenameHash": event_data["filenameHash"]}
        collection.update(key, event_data, upsert=True)
    sleep(0.1)
