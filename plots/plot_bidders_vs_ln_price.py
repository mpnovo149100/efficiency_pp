import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 
import statsmodels.api as sm

def plot_bidders_vs_ln_price(df: pd.DataFrame):
    """
    Figure 4.12: Relação entre número de concorrentes e log do preço efetivo.
    Inclui regressão linear com banda de confiança.
    """

    # 1. Filtrar valores válidos
    df_plot = df[["bidders", "ln_effective_total_price"]].dropna()

    # 2. Modelo de regressão linear
    X = sm.add_constant(df_plot["bidders"])
    y = df_plot["ln_effective_total_price"]
    model = sm.OLS(y, X).fit()

    # 3. Prever valores e intervalo de confiança
    x_pred = np.linspace(df_plot["bidders"].min(), df_plot["bidders"].max(), 100)
    X_pred = sm.add_constant(x_pred)
    y_pred = model.predict(X_pred)

    # Intervalo de confiança 95%
    pred_summary = model.get_prediction(X_pred).summary_frame(alpha=0.05)
    y_lower = pred_summary["obs_ci_lower"]
    y_upper = pred_summary["obs_ci_upper"]

    # 4. Gráfico
    fig = go.Figure()

    # Scatterplot
    fig.add_trace(go.Scatter(
        x=df_plot["bidders"],
        y=df_plot["ln_effective_total_price"],
        mode="markers",
        name="Data Points",
        marker=dict(color="black", opacity=0.4)
    ))

    # Linha de regressão
    fig.add_trace(go.Scatter(
        x=x_pred,
        y=y_pred,
        mode="lines",
        name="Linear Regression",
        line=dict(color="darkred", width=2)
    ))

    # Banda de confiança
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_pred, x_pred[::-1]]),
        y=np.concatenate([y_lower, y_upper[::-1]]),
        fill='toself',
        fillcolor='rgba(200,0,0,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        name="95% Confidence Interval"
    ))

    fig.update_layout(
        title="Relationship between Number of Bidders and Log of Effective Contract Price",
        xaxis_title="Number of Bidders",
        yaxis_title="Log of Effective Price",
        template="simple_white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
