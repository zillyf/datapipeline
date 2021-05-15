FROM python:3.7

RUN pip install pymongo kafka-python Pillow pandas wget

EXPOSE 8000

COPY ./app /app

CMD ["python3", "app/sendFilesConsumer.py"]
#CMD ["python3", ${DATAPIPENODECOMMAND}]
