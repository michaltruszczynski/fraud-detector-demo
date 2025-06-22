FROM python:3.10-slim

WORKDIR /app

COPY producer/producer.py .
COPY data/creditcard.csv /data/

RUN pip install pandas kafka-python

CMD ["python3", "-u", "producer.py"]