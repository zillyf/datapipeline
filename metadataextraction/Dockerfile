FROM ultralytics/yolov5

RUN pip install fastapi uvicorn pymongo  aiofiles kafka-python Pillow python-multipart

EXPOSE 8000

COPY ./app /usr/src/app

CMD ["python3", "/usr/src/app/serveYolo.py"]

