import pandas as pd
import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def export_shap_importance_to_csv(
    input_path="Data/dados_completos.csv",
    output_path="Data/shap_importance_rf.csv"
):
    df = pd.read_csv(input_path)
    df['cost_increase'] = (df['effective_total_price'] > df['base_price']).astype(int)

    features = [
        'base_price', 'act_type', 'CPV_agrupado', 'bidders',
        'execution_dummy', 'contract_year', 'loc',
        'covid_pandemic', 'environmental'
    ]

    cat_vars = ['act_type', 'CPV_agrupado', 'loc']
    df_model = df[features + ['cost_increase']].dropna().copy()

    label_encoders = {}
    for col in cat_vars:
        le = LabelEncoder()
        df_model[col] = le.fit_transform(df_model[col])
        label_encoders[col] = le

    X = df_model[features]
    y = df_model['cost_increase']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar o modelo
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)

    # SHAP
    explainer = shap.TreeExplainer(rf)
    shap_values = explainer.shap_values(X_train)

    # Selecionar shap_values da classe 1
    sv = shap_values[1] if isinstance(shap_values, list) else shap_values

    # Verificação correta da forma
    assert sv.shape == X_train.shape, f"SHAP shape {sv.shape} != X_train shape {X_train.shape}"

    # Calcular importância média absoluta
    shap_importance = pd.DataFrame({
        'feature': X_train.columns,
        'mean_abs_shap': np.abs(sv).mean(axis=0)
    }).sort_values(by='mean_abs_shap', ascending=False)

    shap_importance.to_csv(output_path, index=False)
    print("SHAP importances salvas em:", output_path)

# Executar
export_shap_importance_to_csv()