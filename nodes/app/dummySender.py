from time import sleep
from json import dumps
from kafka import KafkaProducer

topic = "send_kitti_dataset_request"
# topic= 'send_file'
# topic= 'topic_test'

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)
for i in range(1):
    newEntry = {
        "KittiDatasetURL": "https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/2011_09_26_drive_0002/2011_09_26_drive_0002_sync.zip",
        "datasetprovider": "test",
        "datasetname": "test" + str(i),
        "filenameHash": "test" + str(i),
    }
    producer.send(topic, value=newEntry)
    sleep(1)
    print("send:")
    print(newEntry)
