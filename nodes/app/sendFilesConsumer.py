# pip3 install kafka
from kafka import KafkaConsumer
from json import loads
from time import sleep

# pip3 install pymongo
from pymongo import MongoClient
client = MongoClient('localhost:27017')
collection = client.images.images


consumer = KafkaConsumer(
    'topic_test',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    #collection.insert_one(  event_data )
    key={'filenameHash': event_data['filenameHash'] }
    collection.update(key, event_data, upsert=True);
    sleep(0.1)