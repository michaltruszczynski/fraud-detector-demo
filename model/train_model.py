
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

# Ścieżki
input_csv = "/data/creditcard.csv"
output_model = "/model/model.pkl"

# Wczytaj dane
df = pd.read_csv(input_csv)
features = [f'V{i}' for i in range(1, 29)] + ['Amount']
X = df[features]
y = df['Class']

# Trenuj model
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Zapisz model
os.makedirs("/model", exist_ok=True)
joblib.dump(model, output_model)
print("Model saved to", output_model)
