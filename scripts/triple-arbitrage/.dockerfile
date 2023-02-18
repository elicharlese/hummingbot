FROM python:3.8-slim-buster

WORKDIR /app

COPY manual.py .

RUN pip install --no-cache-dir kucoin-python hummingbot-client

CMD ["python", "manual.py"]
