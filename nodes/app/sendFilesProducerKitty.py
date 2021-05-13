from  sendFiles import *

import os
from time import sleep
from json import dumps
from kafka import KafkaProducer
from PIL import Image
import hashlib
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

#cityscape_dir= 'C:/Users/zilly/Downloads/leftImg8bit_trainvaltest/leftImg8bit'
#cityscape_dir= 'C:/Users/zilly/Downloads/leftImg8bit_trainvaltest/leftImg8bit/test/berlin'

directories={}
directories["ingest_dir"]='z:/kitti'
directories["blobstorage_dir"]='z:/blobstorage'
directories["thumbnail_dir"]=directories["blobstorage_dir"]+'/thumbnails'

ingest_dir = directories["ingest_dir"]
dataset_dir = ingest_dir+'/'+'2011_09_26_drive_0005_sync/2011_09_26/2011_09_26_drive_0005_sync/image_02/data/'

################# KITTI RELATED START ####################
import pandas as pd

basedirectory = 'z:/kitti/2011_09_26_drive_0005_sync/2011_09_26/2011_09_26_drive_0005_sync/'


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

blobstorage_dir='z:/blobstorage'
thumbnail_dir='z:/blobstorage/thumbnails'

import glob
files = glob.glob(dataset_dir + '/**/*.png', recursive=True)

#sendFiles(files, basicmetadata, df_merged)
kafkaSendFiles(directories, files, basicmetadata, df_merged, producer)