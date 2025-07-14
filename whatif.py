import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def what_if_dashboard():
    # --------------  CONFIG  -----------------
    THRESHOLD = 0.065                # Youden-J threshold
    MODEL_PATH = "rf_model.pkl"      # RF classifier (pickle)
    PREP_PATH  = "preprocess.pkl"    # ColumnTransformer / Pipeline

    # ----------  LOAD CSV ---------------------
    try:
        df = pd.read_csv("Data/dados.csv")
    except FileNotFoundError:
        st.error("Ficheiro 'dados.csv' não encontrado.")
        return

    SAFE_COST = df[(df["risk_prob"] < THRESHOLD) & (df["efficiency"] >= 0.6)]["effective_total_price"].mean()
    # -----------------------------------------

    # ----------  LOAD MODEL & PIPELINE -------
    @st.cache_resource
    def load_artifacts():
        model = joblib.load(MODEL_PATH)
        pre   = joblib.load(PREP_PATH)
        return model, pre

    model_rf, preproc = load_artifacts()

    # ----------  UI – SIDEBAR -----------------
    st.sidebar.header("What-if inputs")

    loc_options = sorted(df["loc"].dropna().unique())
    cpv_options = sorted(df["CPV_agrupado"].dropna().unique())
    act_type_options = sorted(df["act_type"].dropna().unique())

    locations = st.sidebar.multiselect("Location(s) (NUTS II)", loc_options, default=["PT17"])
    cpv = st.sidebar.selectbox("CPV Group", cpv_options, index=cpv_options.index("Services") if "Services" in cpv_options else 0)
    act_type = st.sidebar.selectbox("Type of Act", act_type_options)

    bidders = st.sidebar.slider("Number of Bidders", 1, 80, 3)
    year = st.sidebar.slider("Contract Year", 2011, 2024, 2023)
    eff_range = st.sidebar.slider("Efficiency range", 0.0, 1.0, (0.0, 1.0), step=0.05)
    efficiency_val = np.mean(eff_range)

   

    # ----------  CONSTRUIR DATAFRAME ---------
    input_list = []
    for loc in locations:
        input_list.append({
            "loc": loc,
            "bidders": bidders,
            "contract_year": year,
            "ln_base_price": np.log(50_000),
            "act_type": act_type,
            "environmental": 1,
            "execution_dummy": 0,
            "covid_pandemic": 1 if year >= 2020 else 0,
            "CPV_agrupado": cpv,
            "efficiency": efficiency_val
        })

    df_input = pd.DataFrame(input_list)

    # ----------  PREDIÇÃO --------------------
    X = preproc.transform(df_input)
    probs = model_rf.predict_proba(X)[:, 1]

    # ----------  RESULTADOS ------------------
    df_input["Predicted Risk"] = probs
    df_input["Risk Class"] = np.where(probs >= THRESHOLD, "⚠️ High Risk", "✅ Low Risk")
    df_input["Expected Cost (€)"] = np.where(probs >= THRESHOLD, SAFE_COST, 50_000)

    # ----------  MOSTRAR ---------------------
    st.markdown("### Scenario Results")
    st.dataframe(df_input[["loc", "Predicted Risk", "Risk Class", "Expected Cost (€)"]], use_container_width=True)

    # ----------  GRÁFICO ---------------------
    fig = px.bar(
        df_input,
        x="loc",
        y="Expected Cost (€)",
        color="Risk Class",
        text="Expected Cost (€)",
        color_discrete_map={"✅ Low Risk": "#1f77b4", "⚠️ High Risk": "#d62728"}
    )
    fig.update_traces(texttemplate='%{text:,}', textposition="outside")
    fig.update_layout(
        title="Expected Cost by Location",
        xaxis_title="Location (NUTS II)",
        yaxis_title="Expected Cost (€)",
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # ----------  INFO FINAL -------------------
    st.info("Use the sidebar to explore how different inputs affect the risk of cost increases and the expected cost.")