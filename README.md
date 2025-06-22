
# 🛡️ Fraud Detection System (ver 1)

System do wykrywania oszustw z wykorzystaniem danych transakcji kart kredytowych. Architektura opiera się na mikroserwisach uruchamianych w kontenerach Docker, wykorzystujących Apache Spark, model ML i WebSocket do wizualizacji wykrytych oszustw w czasie rzeczywistym.

---

## 📥 Ważne - plik z danymi trzeba pobrać przed uruchomieniem

Ze względu na wielkość pliku, plik z danymi **nie jest dołączony** do repozytorium.

1. Przejdź na [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)  
2. Pobierz plik `creditcard.csv`  
3. Umieść go w katalogu projektu:

```
data/creditcard.csv
```

---

## 🧠 Trenowanie modelu

Model uczenia maszynowego (logistyczna regresja) trenowany jest wewnątrz kontenera o nazwie `trainer`. Skrypt `train_model.py` wczytuje dane z `/data/creditcard.csv` i zapisuje model do `/model/model.pkl`.

Aby wytrenować model:

```bash
docker compose build 
docker compose run trainer
```

⚠️ Upewnij się, że plik `creditcard.csv` znajduje się w `data/` przed uruchomieniem. Po zbudowaniu modelu kontener trainer można zatrzymać.

---

## 🚀 Uruchamianie systemu

Po wytrenowaniu modelu uruchom wszystkie komponenty systemu jednocześnie:

```bash
docker compose up -d kafka producer consumer websocket
```

To polecenie uruchomi usługi:

- `producer` – generuje dane transakcji
- `consumer` – analizuje dane z użyciem Spark i modelu ML
- `websocket` – serwer WebSocket + frontend
- `kafka` – pośredniczy w przesyłaniu danych między serwisami

---

## 🌐 Interfejs użytkownika

Po uruchomieniu przejdź w przeglądarce do:

```
http://localhost:5000
```

Zobaczysz wizualizację wykrytych transakcji podejrzanych w czasie rzeczywistym.

---

## 📁 Struktura projektu

```
fraud-demo_ver_1/
│
├── consumer_spark/        # Spark: analiza i wykrywanie oszustw
├── producer/              # Symulacja strumienia transakcji
├── model/                 # Trening modelu ML
│   ├── train_model.py     # Skrypt treningowy
│   └── model.pkl          # Wygenerowany model
├── websocket/             # Serwer WebSocket + frontend
├── data/                  # Tutaj umieść creditcard.csv
└── docker-compose.yml     # Konfiguracja usług
```

---

## 🧰 Technologie

- **Apache Spark (PySpark)** – analiza danych w strumieniu  
- **Scikit-learn** – trenowanie modelu ML  
- **Docker & Docker Compose (v2)** – konteneryzacja  
- **WebSocket + HTML (Flask)** – interfejs użytkownika  
- **Kafka** – wymiana danych między serwisami  

---

## 📌 Uwagi końcowe

✅ Model **musi zostać wytrenowany jako pierwszy**, przed uruchomieniem pozostałych usług.  
❌ Bez pliku `model.pkl` system nie będzie działać poprawnie.  
📦 Dane `creditcard.csv` muszą zostać ręcznie pobrane z Kaggle i umieszczone lokalnie.
