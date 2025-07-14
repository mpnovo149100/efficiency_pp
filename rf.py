# rf.py  ────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
import joblib
from pathlib import Path

def run_rf_mitigation(
        csv_in="Data/dados_completos.csv",
        csv_out="Data/randomforest_results.csv",
        model_out="models/random_forest_model.pkl",
        threshold_rf=0.065,
        random_state=123
):
    """
    Train RF, compute risk probabilities, apply cost-mitigation rule and save results.
    Mirrors the original R workflow.
    """
    # ── 1) Load & prepare -------------------------------------------------------
    df = pd.read_csv(csv_in)

    # Target: 1 if effective_total_price > base_price
    df["cost_increase"] = (df["effective_total_price"] > df["base_price"]).astype(int)

    # Feature set (≃ R script)
    features = [
        "ln_base_price",    # already in € log-scale
        "act_type",
        "bidders",
        "execution_dummy",
        "effective_total_price",  # used for price simulation
        "contract_year",
        "CPV_agrupado",
        "loc",
        "covid_pandemic",
        "environmental",
    ]
    # Keep only rows with no NA in selected columns + cost_increase
    df_model = df[features + ["cost_increase"]].dropna().copy()

    # ── 2) Encode categoricals --------------------------------------------------
    cat_mask   = df_model[features].dtypes == "object"
    cat_cols   = cat_mask[cat_mask].index.tolist()

    if cat_cols:
        enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        df_model[cat_cols] = enc.fit_transform(df_model[cat_cols])

    X = df_model[features]
    y = df_model["cost_increase"]

    # ── 3) Train RF -------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=random_state
    )

    rf = RandomForestClassifier(
        n_estimators=100,      # as in R (ntree = 100)
        max_depth=None,
        random_state=random_state,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    # Probabilities for **ALL** usable rows (train+test)
    risk_prob = rf.predict_proba(X)[:, 1]

    # ── 4) Mitigation rule ------------------------------------------------------
    df_model["risk_prob"] = risk_prob

    # Average price for *safe* contracts
    mean_safe_price = df_model.loc[df_model.risk_prob < threshold_rf,
                                   "effective_total_price"].mean()

    df_model["price_sim_rf"] = np.where(
        df_model["risk_prob"] >= threshold_rf,
        mean_safe_price,
        df_model["effective_total_price"]
    )

    # ── 5) Aggregate costs ------------------------------------------------------
    real_cost_rf = df_model["effective_total_price"].sum()
    sim_cost_rf  = df_model["price_sim_rf"].sum()
    savings_rf   = real_cost_rf - sim_cost_rf

    # ── 6) Persist / report -----------------------------------------------------
    out_cols = list(df.columns) + ["risk_prob", "price_sim_rf"]
    # align indices to original df for a clean merge
    df_full = df.join(df_model[["risk_prob", "price_sim_rf"]])

    Path(csv_out).parent.mkdir(parents=True, exist_ok=True)
    df_full.to_csv(csv_out, index=False)

    Path(model_out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(rf, model_out)

    def euro(x):  # simple € formatter
        return f"€ {x:,.0f}".replace(",", " ")

    print("Random-Forest Mitigation Scenario")
    print(" • Real Cost:      ", euro(real_cost_rf))
    print(" • Simulated Cost: ", euro(sim_cost_rf))
    print(" • Savings:        ", euro(savings_rf))

    return {
        "model": rf,
        "encoder": enc if cat_cols else None,
        "results_df": df_full,
        "real_cost": real_cost_rf,
        "sim_cost": sim_cost_rf,
        "savings": savings_rf,
    }

# Quick run (comment-out when importing from elsewhere)
if __name__ == "__main__":
    run_rf_mitigation()