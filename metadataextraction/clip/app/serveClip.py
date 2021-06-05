import torch
import clip
from PIL import Image

import os
import aiofiles
import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

clipPort = os.getenv("CLIP_PORT", "8003")
out_file_path = "data/images/"

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    async with aiofiles.open(out_file_path + file.filename, "wb") as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    print("uploaded filename" + file.filename)
    img = preprocess(Image.open(out_file_path + file.filename)).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(img)

    return image_features.numpy().tolist()

    #results = model(img, size=640)  # reduce size=320 for faster inference
    #return results.pandas().xyxy[0].to_json(orient="records")

if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    uvicorn.run(app, host="0.0.0.0", port=int(clipPort))
