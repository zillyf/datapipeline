FROM python:3.7

RUN pip install fastapi uvicorn pymongo aiofiles

EXPOSE 8000

COPY ./app /app

CMD ["python3", "app/main.py"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
