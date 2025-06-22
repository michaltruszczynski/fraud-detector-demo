from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, DoubleType, IntegerType
from datetime import datetime
import pandas as pd
import joblib
import requests

# Załaduj model
model = joblib.load("/model/model.pkl")

# Funkcja do wysyłania fraudów do WebSocket serwera
def send_to_websocket(data):
    try:
        requests.post("http://websocket:5000/fraud", json=data)
    except Exception as e:
        print(f"Błąd przy wysyłaniu do websocket: {e}")

# Przetwarzanie batcha
def classify_batch(df, epoch_id):
    if df.count() == 0:
        return

    pdf = df.toPandas()
    features = [f'V{i}' for i in range(1, 29)] + ['Amount']
    preds = model.predict(pdf[features])
    pdf['prediction'] = preds

    frauds = pdf[pdf['prediction'] == 1]
    if not frauds.empty:
        print("WYKRYTO FRAUDY:")
        print(frauds.to_string(index=False))

        for _, row in frauds.iterrows():
            fraud_data = row[features + ['Amount']].to_dict()
            fraud_data['DetectedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_to_websocket(fraud_data)

# Struktura danych JSON z Kafka
schema = StructType()
for i in range(1, 29):
    schema = schema.add(f"V{i}", DoubleType())
schema = schema.add("Amount", DoubleType()).add("Class", IntegerType())

# Spark
spark = SparkSession.builder.appName("FraudDetector").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "transactions") \
    .load()

parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

query = parsed_df.writeStream \
    .foreachBatch(classify_batch) \
    .trigger(processingTime="2 seconds") \
    .start()

query.awaitTermination()