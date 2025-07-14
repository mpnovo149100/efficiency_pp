import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import streamlit as st

# cor “corporate blue” usada nos outros plots
BLUE = "#0B2C54"

def plot_ln_base_vs_ln_effective(df):

    df = df.dropna(subset=['ln_base_price', 'ln_effective_total_price']).copy()

    # Regressão linear
    X = sm.add_constant(df['ln_base_price'])
    y = df['ln_effective_total_price']
    model = sm.OLS(y, X).fit()
    df['predicted_ln_effective'] = model.predict(X)

    # Scatter com a paleta azul definida
    fig = px.scatter(
        df,
        x='ln_base_price',
        y='ln_effective_total_price',
        opacity=0.55,                     # leve transparência
        color_discrete_sequence=[BLUE],   # pontos azuis
        labels={
            'ln_base_price': 'Logₑ(Base Price)',
            'ln_effective_total_price': 'Logₑ(Effective Price)'
        },
        title="Relationship between Log(Base Price) and Log(Effective Price)"
    )

    # Linha de regressão (mesmo tom azul, mas ligeiramente mais clara)
    fig.add_scatter(
        x=df['ln_base_price'],
        y=df['predicted_ln_effective'],
        mode='lines',
        name='OLS Trend',
        line=dict(color=BLUE, width=3)
    )

    # Layout
    fig.update_layout(
        font=dict(color='white'),
        xaxis_title='Logₑ(Base Price)',
        yaxis_title='Logₑ(Effective Price)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)