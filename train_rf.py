# train_rf_model.py
import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score

# === 1. Load data ===
df = pd.read_csv("Data/dados.csv")

# Target
y = df["custo_aumentou"]

# Features para o modelo
features = [
    "loc", "bidders", "contract_year", "ln_base_price",
    "act_type", "environmental", "execution_dummy", 
    "covid_pandemic", "CPV_agrupado"
]
X = df[features]

# === 2. Pré-processamento ===

# Variáveis categóricas e numéricas
cat_vars = ["loc", "act_type", "CPV_agrupado"]
num_vars = ["bidders", "contract_year", "ln_base_price"]
bin_vars = ["environmental", "execution_dummy", "covid_pandemic"]

# Pipeline
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_vars),
    ("num", StandardScaler(), num_vars),
    ("bin", "passthrough", bin_vars)
])

# === 3. Modelo ===
model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("rf", RandomForestClassifier(n_estimators=100, random_state=42))
])

# === 4. Treinar ===
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
model.fit(X_train, y_train)

# === 5. Avaliar ===
y_prob = model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_prob)
print(f"AUC ROC: {roc_auc:.3f}")

# === 6. Guardar artefactos ===
joblib.dump(model.named_steps["rf"], "rf_model.pkl")
joblib.dump(preprocessor, "preprocess.pkl")