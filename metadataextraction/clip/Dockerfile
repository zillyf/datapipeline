FROM python:3.8.0-slim

RUN apt-get clean && \
    apt-get update -y && \
    apt-get install -y wget git curl

RUN pip install git+https://github.com/openai/CLIP.git
RUN pip install wget fastapi uvicorn aiofiles Pillow python-multipart

WORKDIR /usr/src/app

COPY ./app /usr/src/app

CMD ["python3", "/usr/src/app/serveClip.py"]