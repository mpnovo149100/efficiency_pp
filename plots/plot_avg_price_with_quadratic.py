import plotly.graph_objects as go
import numpy as np
import streamlit as st
import pandas as pd


def plot_avg_price_with_quadratic(df):
    if 'contract_date' not in df.columns or 'effective_total_price' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias.")
        return

    # Criar ou atualizar a coluna 'contract_year' com base no df filtrado
    df = df.copy()  # evitar alterações no df original
    

    # Agrupar por ano e calcular média do preço efetivo
    avg_price_by_year = df.groupby('contract_year')['effective_total_price'].mean().dropna().sort_index()

    if avg_price_by_year.empty:
        st.info("Não há dados disponíveis para este intervalo de datas.")
        return

    x = avg_price_by_year.index.values
    y = avg_price_by_year.values

    # Ajuste polinomial quadrático (grau 2)
    coefs = np.polyfit(x, y, deg=2)
    poly_func = np.poly1d(coefs)
    x_smooth = np.linspace(x.min(), x.max(), 100)
    y_smooth = poly_func(x_smooth)

    # Gráfico base
    fig = go.Figure()

    # Linha azul: média por ano
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name='Avg. Effective Price',
        line=dict(color='darkblue')
    ))

    # Linha de tendência polinomial (vermelha)
    fig.add_trace(go.Scatter(
        x=x_smooth,
        y=y_smooth,
        mode='lines',
        name='Quadratic Trend',
        line=dict(color='darkred', width=3)
    ))

    fig.update_layout(
        title="Average Effective Contract Price Over Time with Quadratic Trendline",
        xaxis_title="Contract Year",
        yaxis_title="Average Effective Price",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig, use_container_width=True)