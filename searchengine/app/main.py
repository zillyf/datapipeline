from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles

from pymongo import MongoClient

from kafka import KafkaProducer

import urllib.parse

import os
import sys
from time import sleep
import json
from json import dumps

app = FastAPI()

kafkaTopicKittiDatasetRequest = os.getenv(
    "KAFKA_TOPIC_KITTIDATASETREQUEST", "send_kitti_dataset_request"
)
kafkaWaitTime = int(os.getenv("KAFKA_WAIT_TIME", 10))
kafkaServer = os.getenv("KAFKA_SERVER", "localhost:9092")
print("kafkaTopicKittiDatasetRequest: " + kafkaTopicKittiDatasetRequest)

# wait for startup of Kafka
sys.stdout.write("Kitti Dataset Request: wait for startup of Kafka\n")
sleep(kafkaWaitTime)

producer = KafkaProducer(
    bootstrap_servers=[kafkaServer], value_serializer=lambda x: dumps(x).encode("utf-8")
)

curDir = os.getcwd()
appDir = curDir + "/app"
blobDir = ""
imgageThumbnailDir = "/data/imagethumbnails/"

app.mount("/static", StaticFiles(directory="app/static"), name="static")


dbServer = os.getenv("MONGO_DB_SERVER", "localhost:27017")
dbUser = os.getenv("MONGO_USERNAME", "root")
dbPW = os.getenv("MONGO_PASSWORD", "rootpassword")

searchPort = os.getenv("SEARCHENGINE_PORT", "8000")

client = MongoClient(dbServer, username=dbUser, password=dbPW)

print("Mongo DB Connection -----")
print("server:" + dbServer)
print("user:" + dbUser)

collection = client.images.images


@app.get("/", response_class=HTMLResponse)
def read_root():

    f = open(appDir + "/index.html", "r")
    returnString = f.read()
    return returnString
    # print(returnString)
    # return {"Hello": "World"}


@app.get("/imagelistpage/{page_id}")
def read_imagelistpage(page_id: int):
    pagesize = 50
    skipoffset = (page_id - 1) * pagesize
    data = []
    for image in (
        collection.find(
            {},
            {
                "datasetprovider": 1,
                "filenameHash": 1,
                "datasetname": 1,
                "imageFilename": 1,
                "timestamp": 1,
                "_id": 0,
            },
        )
        .skip(skipoffset)
        .limit(pagesize)
    ):
        data.append(image)

    # f = open( appDir + '/books.json', 'r')
    # f2 = json.load(f)
    #    returnString = f.read()
    #
    returnString = json.dumps(data)
    returnString = data
    # print(returnString);
    return returnString


@app.get("/imagethumbnail/{image_id}")
def read_image(image_id: str):
    filename = imgageThumbnailDir + image_id + ".jpg"
    # f = open( imgageThumbnailDir + image_id+'.jpg', 'r')
    # data = f.read()
    return FileResponse(filename)


@app.post("/requestdatasetkitti/{KittiDatasetURL}")
async def request_dataset_kitti(KittiDatasetURL: str):
    newEntry = {"KittiDatasetURL": urllib.parse.unquote(KittiDatasetURL)}
    producer.send(kafkaTopicKittiDatasetRequest, value=newEntry)


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(searchPort))
