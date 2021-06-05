import os
import aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile
import torch
from PIL import Image

app = FastAPI()

yoloPort = os.getenv("YOLO_PORT", "8002")
out_file_path = "data/images/"

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    async with aiofiles.open(out_file_path + file.filename, "wb") as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    print("uploaded filename" + file.filename)
    img = Image.open(out_file_path + file.filename)
    results = model(img, size=640)  # reduce size=320 for faster inference
    return results.pandas().xyxy[0].to_json(orient="records")

if __name__ == "__main__":
    model = torch.hub.load(
        "ultralytics/yolov5", "yolov5s", force_reload=True
    )  # force_reload to recache
    uvicorn.run(app, host="0.0.0.0", port=int(yoloPort))
