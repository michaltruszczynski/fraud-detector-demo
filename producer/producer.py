import json
import time
import random
from kafka import KafkaProducer
import pandas as pd
from datetime import datetime, timedelta

# Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Dane
df = pd.read_csv('/data/creditcard.csv')
frauds = df[df['Class'] == 1].to_dict(orient='records')
non_frauds = df[df['Class'] == 0].to_dict(orient='records')

# Czas końca
end_time = datetime.now() + timedelta(minutes=30)
next_fraud_time = datetime.now() + timedelta(seconds=random.randint(10, 25))

print("Producer: start z 1 fraudem co 10–25 sek.\n", flush=True)

while datetime.now() < end_time:
    now = datetime.now()
    if now >= next_fraud_time:
        # Wyślij fraud
        row = random.choice(frauds)
        next_fraud_time = now + timedelta(seconds=random.randint(10, 25))
    else:
        # Wyślij normalną transakcję
        row = random.choice(non_frauds)

    data = {f'V{k}': row[f'V{k}'] for k in range(1, 29)}
    data['Amount'] = row['Amount']
    data['Class'] = int(row['Class'])

    producer.send('transactions', value=data)
    print(f"Wysłano: Class={data['Class']}, Amount={data['Amount']:.2f}", flush=True)

    time.sleep(random.uniform(0.2, 0.5))

print("\n Produkcja zakończona (30 minut)", flush=True)