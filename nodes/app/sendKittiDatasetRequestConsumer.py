from sendFiles import *


# 'os' is a library which contains functions to interact with operating system, including file system
import os
import sys
from time import sleep
from json import dumps
from json import loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
from PIL import Image
import hashlib
import wget
import zipfile
import pandas as pd
from pathlib import Path


kafkaTopicKittiDatasetRequest = os.getenv(
    "KAFKA_TOPIC_KITTIDATASETREQUEST", "send_kitti_dataset_request"
)

# wait for startup of Kafka
kafkaWaitTime = int(os.getenv("KAFKA_WAIT_TIME", 10))
sys.stdout.write("Wait for startup of Kafka: "+ str(kafkaWaitTime) +" seconds\n")
sleep(kafkaWaitTime)


kafkaServer = os.getenv("KAFKA_SERVER", "localhost:9092")

downloaddir = "/data/downloads/"
kittyextractdir = "/data/extractedfiles/"

directories = {}
directories["ingest_dir"] = kittyextractdir
directories["blobstorage_dir"] = "/data/imageblobstorage/"
directories["thumbnail_dir"] = "/data/imagethumbnails/"

metadataYoloServer = os.getenv("METADATA_YOLO", "localhost:8002")
directories["METADATA_YOLO"]=metadataYoloServer

metadataClipServer = os.getenv("METADATA_CLIP", "localhost:8003")
directories["METADATA_CLIP"]=metadataClipServer

# directories["thumbnail_dir"]=os.getenv('DATAPIPE_THUMBNAILDIR','/home/zilly/blobstoragethumbnail')


kafkaTopicSendFiles = os.getenv("KAFKA_TOPIC_SENDFILES", "send_file")

print("kafkaTopicSendFiles: " + kafkaTopicSendFiles)

print("kafkaTopicKittiDatasetRequest: " + kafkaTopicKittiDatasetRequest)


producer = KafkaProducer(
    bootstrap_servers=[kafkaServer], value_serializer=lambda x: dumps(x).encode("utf-8")
)

consumer = KafkaConsumer(
    kafkaTopicKittiDatasetRequest,
    bootstrap_servers=[kafkaServer],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="my-group-id",
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)


# blobstorage_dir='z:/blobstorage'
# thumbnail_dir='z:/blobstorage/thumbnails'

################# KITTI RELATED START ####################

columnnames = [
    "lat",
    "lon",
    "alt",
    "roll",
    "pitch",
    "yaw",
    "vn",
    "ve",
    "vf",
    "vl",
    "vu",
    "ax",
    "ay",
    "az",
    "af",
    "al",
    "au",
    "wx",
    "wyw",
    "wz",
    "wf",
    "wl",
    "wu",
    "pos_accuracy",
    "vel_accuracy",
    "navstat",
    "numsats",
    "posmode",
    "velmode",
    "orimode",
]

df = pd.DataFrame(columns=columnnames)

# the data for our odometry data is in this subfolder
metadatadir = "oxts/data"


for event in consumer:
    event_data = event.value
    # Do whatever you want
    print(event_data)
    # collection.insert_one(  event_data )
    if "KittiDatasetURL" in event_data:
        KittiDatasetURL = event_data["KittiDatasetURL"]
        sleep(0.1)
    else:
        continue

    (baseURL, filename) = os.path.split(KittiDatasetURL)
    (datasetname, fileextension) = os.path.splitext(filename)
    zipfilename = downloaddir + filename


    filecheck=Path(zipfilename)
    if filecheck.is_file:
        print('Skip! Using previously downloaded file: '+zipfilename)
    else:
        print('Downloading file: '+zipfilename)
        a = wget.download(KittiDatasetURL, zipfilename)

    filecheck=Path(kittyextractdir + datasetname)
    if filecheck.is_file:
        print('Skip! Using previously extracted file: '+kittyextractdir + datasetname)
    else:
        print('Extracting file: '+kittyextractdir + datasetname)
        zf = zipfile.ZipFile(zipfilename, "r")
        zf.extractall(kittyextractdir + datasetname)

    daydir = datasetname[0:10]
    # two strings can easily be concatinated using '+' operator
    basedirectory = (
        kittyextractdir + datasetname + "/" + daydir + "/" + datasetname + "/"
    )

    directory = basedirectory + metadatadir
    # iterate over all files in the directory.
    # Nota Bene: os.scandir is for Python 3.5 and above. Use os.listdir() for older python versions
    for entry in os.scandir(directory):
        if entry.path.endswith(".txt") and entry.is_file():
            # print(entry.path)
            new_df = pd.read_csv(entry.path, delimiter=" ", names=columnnames)
            df = df.append(new_df, ignore_index=True)

    # now let's include more data, such as timestamps

    timestampfile = basedirectory + "oxts/timestamps.txt"

    timestamps_df = pd.read_csv(timestampfile, names=["ts"])
    # Cut off three last digits (keep microseconds, but not nanoseconds)
    timestamps_df_micro = timestamps_df.ts.str[:-3]

    # Let's create a merged dataframe, use index from both dataframes as merge key
    df_merged = df.merge(timestamps_df_micro, left_index=True, right_index=True)

    ################# KITTI RELATED STOP ####################

    basicmetadata = {
        "datasetprovider": "Kitti",
        "datasetproviderURL": "http://www.cvlibs.net/datasets/kitti/raw_data.php",
        "datasetname": datasetname,
        "datasetcontainer": filename,
    }

    dataset_dir = basedirectory + "/" + "/image_02/data/"
    import glob

    files = sorted(glob.glob(dataset_dir + "/**/*.png", recursive=True))

    # sendFiles(files, basicmetadata, df_merged)
    kafkaSendFiles(
        directories, files, basicmetadata, df_merged, producer, kafkaTopicSendFiles
    )
