from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pymongo import MongoClient

import os
import json
app = FastAPI()

curDir = os.getcwd()
appDir = curDir
blobDir = ''

client = MongoClient('localhost:27017')
collection = client.images.images

def getHTMLHeader(title='Hello World'):
    returnString = ''
    returnString=returnString+'<html><title>'+title+'</title><body>'
    return returnString

def getHTMLFooter():
    returnString = ''
    returnString=returnString+'</body></html>'
    return returnString


@app.get("/", response_class=HTMLResponse)
def read_root():

    returnString = getHTMLHeader()+'test'+getHTMLFooter()
    f = open( appDir+'/index.html', 'r')
    returnString = f.read()
    return returnString
    #print(returnString)
    #return {"Hello": "World"}

@app.get("/booksearch", response_class=HTMLResponse)
def read_root():

    returnString = getHTMLHeader()+'test'+getHTMLFooter()
    f = open( appDir+'/books.html', 'r')
    returnString = f.read()
    return returnString
    #print(returnString)
    #return {"Hello": "World"}

@app.get("/imagelistpage/{page_id}")
def read_imagelistpage(page_id: int):
    pagesize=50
    skipoffset=(page_id-1)*pagesize
    data = []
    for image in collection.find({"datasetprovider":"Cityscapes"}, {'datasetprovider':1, 'filenameHash':1, 'datasetname':1, 'imageFilename':1, '_id':0}).skip(skipoffset).limit(pagesize):
        data.append(image)

    #f = open( appDir + '/books.json', 'r')
    #f2 = json.load(f)
    #    returnString = f.read()
    #
    returnString = json.dumps( data )
    returnString = data
    #print(returnString);
    return returnString

@app.get("/books")
def read_books():
    f = open( appDir + '/books.json', 'r')
    f2 = json.load(f)
    #    returnString = f.read()
    returnString = f2
    print(returnString);
    return returnString

@app.get("/image")
def read_image():
    f = open( appDir + '/books.json', 'r')
    data = f.read()
    return Response(content=data, media_type="image/png")



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
