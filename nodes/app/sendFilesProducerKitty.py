from  sendFiles import *

import os
from time import sleep
from json import dumps
from kafka import KafkaProducer
from PIL import Image
import hashlib

kafkaServer = os.getenv('KAFKA_SERVER','localhost:9092')

producer = KafkaProducer(
    bootstrap_servers=[kafkaServer],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

#producer = KafkaProducer(
#    bootstrap_servers=[kafkaServer],
#    value_serializer=lambda x: dumps(x).encode('utf-8'),
#    security_protocol="PLAINTEXT",
#    sasl_mechanism="SCRAM-SHA-256"
#)


#cityscape_dir= 'C:/Users/zilly/Downloads/leftImg8bit_trainvaltest/leftImg8bit'
#cityscape_dir= 'C:/Users/zilly/Downloads/leftImg8bit_trainvaltest/leftImg8bit/test/berlin'

directories={}
directories["ingest_dir"]=os.getenv('KITTI_BASEDIR','~/kitti')
directories["blobstorage_dir"]=os.getenv('DATAPIPE_BLOBSTORAGEDIR','/home/zilly/blobstorage')
directories["thumbnail_dir"]=os.getenv('DATAPIPE_THUMBNAILDIR','/home/zilly/blobstoragethumbnail')

ingest_dir = directories["ingest_dir"]
basedirectory = os.getenv('KITTI_BASEDIR','~/')
dataset_dir = ingest_dir+'/'+'/image_02/data/'

kafkaTopic = os.getenv('KAFKA_TOPIC_SENDFILES','send_file')

print ("kafkaTopic: "+kafkaTopic)

#blobstorage_dir='z:/blobstorage'
#thumbnail_dir='z:/blobstorage/thumbnails'

################# KITTI RELATED START ####################
import pandas as pd



columnnames = ['lat','lon','alt','roll','pitch','yaw', 'vn','ve','vf','vl','vu','ax','ay','az','af','al','au',
           'wx','wyw','wz','wf','wl','wu','pos_accuracy','vel_accuracy','navstat','numsats','posmode','velmode','orimode']

df=pd.DataFrame(columns=columnnames)

# the data for our odometry data is in this subfolder
metadatadir = 'oxts/data'

# import os
# 'os' is a library which contains functions to interact with operating system, including file system
import os

# two strings can easily be concatinated using '+' operator
directory = basedirectory+metadatadir
# iterate over all files in the directory. 
# Nota Bene: os.scandir is for Python 3.5 and above. Use os.listdir() for older python versions 
for entry in os.scandir(directory):
    if (entry.path.endswith(".txt") and entry.is_file()):
        #print(entry.path)
        new_df=pd.read_csv(entry.path,delimiter=' ',names=columnnames)
        df=df.append(new_df, ignore_index=True)

# now let's include more data, such as timestamps

timestampfile = basedirectory + 'oxts/timestamps.txt'

timestamps_df = pd.read_csv(timestampfile, names=['ts'])
# Cut off three last digits (keep microseconds, but not nanoseconds)
timestamps_df_micro=timestamps_df.ts.str[:-3]

# Let's create a merged dataframe, use index from both dataframes as merge key
df_merged=df.merge(timestamps_df_micro, left_index=True, right_index=True)

################# KITTI RELATED STOP ####################

basicmetadata={
    'datasetprovider': 'Kitti',
    'datasetproviderURL': 'http://www.cvlibs.net/datasets/kitti/raw_data.php',
    'datasetname': '2011_09_26_drive_0005_sync',
    'datasetcontainer': '2011_09_26_drive_0005_sync.zip',
}


import glob
files = glob.glob(dataset_dir + '/**/*.png', recursive=True)

#sendFiles(files, basicmetadata, df_merged)
kafkaSendFiles(directories, files, basicmetadata, df_merged, producer, kafkaTopic)