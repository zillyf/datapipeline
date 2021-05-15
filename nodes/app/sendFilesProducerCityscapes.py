from  sendFiles import *

import os
from time import sleep
from json import dumps
from kafka import KafkaProducer
from PIL import Image

consumer = KafkaConsumer(
    'send_file',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

#cityscape_dir= 'C:/Users/zilly/Downloads/leftImg8bit_trainvaltest/leftImg8bit'

directories={}
directories["ingest_dir"]='C:/Users/zilly/Downloads'
directories["blobstorage_dir"]='z:/blobstorage'
directories["thumbnail_dir"]=directories["blobstorage_dir"]+'/thumbnails'

ingest_dir = directories["ingest_dir"]
cityscape_dir= directories["ingest_dir"]+'/'+'leftImg8bit_trainvaltest/leftImg8bit/test/berlin'

basicmetadata={
    'datasetprovider': 'Cityscapes',
    'datasetproviderURL': 'https://www.cityscapes-dataset.com/',
    'datasetname': 'leftImg8bit_trainvaltest',
    'datasetcontainer': 'leftImg8bit_trainvaltest.zip',
}


import glob
files = glob.glob(cityscape_dir + '/**/*.png', recursive=True)

kafkaSendFiles(directories, files, basicmetadata, {}, producer)