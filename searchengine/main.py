from typing import Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import os
import json
app = FastAPI()

curDir = os.getcwd()
appDir = curDir

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

@app.get("/books")
def read_books():
    f = open( appDir + '/books.json', 'r')
    f2 = json.load(f)
    #    returnString = f.read()
    returnString = f2
    print(returnString);
    return returnString


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
