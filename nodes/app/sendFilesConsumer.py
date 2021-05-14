# pip3 install kafka
from kafka import KafkaConsumer
from json import loads
from time import sleep
import os

# pip3 install pymongo
from pymongo import MongoClient

# wait for startup of Kafka
print('wait for startup of Kafka')
sleep(15)

dbServer=os.getenv('MONGO_DB_SERVER','localhost:27017')
dbUser = os.getenv('MONGO_USERNAME','searchengine')
dbPW = os.getenv('MONGO_PASSWORD','searchengine')

kafkaServer = os.getenv('KAFKA_SERVER','localhost:9092')

client = MongoClient(dbServer, username=dbUser, password=dbPW)

print('Mongo DB Connection -----')
print('server:'+dbServer)
print('user:'+dbUser)

collection = client.images.images

kafkaTopic = os.getenv('KAFKA_TOPIC_SENDFILES','topic_test')

print('Kafka Connection -----')
print('server:'+kafkaServer)
print('topic:'+kafkaTopic)


consumer = KafkaConsumer(
    kafkaTopic,
    bootstrap_servers=[kafkaServer],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    security_protocol="PLAINTEXT",
    sasl_mechanism="SCRAM-SHA-256",
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

print('kafka init completed')

for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    #collection.insert_one(  event_data )
    key={'filenameHash': event_data['filenameHash'] }
    collection.update(key, event_data, upsert=True);
    sleep(0.1)