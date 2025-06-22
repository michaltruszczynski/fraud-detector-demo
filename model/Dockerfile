FROM python:3.10-slim

WORKDIR /app

COPY model/train_model.py .
COPY data/creditcard.csv /data/creditcard.csv

RUN pip install pandas scikit-learn joblib

CMD ["python", "train_model.py"]