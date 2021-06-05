from json import dumps
from kafka import KafkaProducer
import pandas as pd

df_temp=pd.read_json('kitti_datasets.json', orient='index')
df=df_temp.rename(columns={0: 'DatasetURL'})

topic = "send_kitti_dataset_request"

producer = KafkaProducer(
    bootstrap_servers=["kafka:9093"],
    value_serializer=lambda x: dumps(x).encode("utf-8"),
)

# choose among the datas from list:

newDatasetID=0;
newEntry = {
    "KittiDatasetURL": df.DatasetURL[newDatasetID],
}
producer.send(topic, value=newEntry)
print("send:")
print(newEntry)