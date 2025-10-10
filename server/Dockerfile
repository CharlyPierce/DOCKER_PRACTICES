FROM python:3.11-slim

WORKDIR /app

RUN pip3 install --no-cache-dir flask

COPY . /app

CMD ["python3", "/app/server.py"]
