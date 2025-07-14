import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st


def plot_log_log_by_region(df: pd.DataFrame):
    """
    Figure 4.21: Log-log relationship between base_price and effective_total_price, by location (NUTS II).
    """
    if not all(col in df.columns for col in ['loc', 'base_price', 'effective_total_price']):
        st.warning("Colunas necessárias ('loc', 'base_price', 'effective_total_price') não encontradas.")
        return

    df_plot = df.copy()
    df_plot = df_plot.dropna(subset=['loc', 'base_price', 'effective_total_price'])
    
    # Adiciona colunas log-transformadas
    df_plot['log_base_price'] = np.log(df_plot['base_price'])
    df_plot['log_effective_price'] = np.log(df_plot['effective_total_price'])

    # Gráfico com facetas por região (NUTS II), trendline e compactação
    fig = px.scatter(
        df_plot,
        x='log_base_price',
        y='log_effective_price',
        facet_col='loc',
        facet_col_wrap=4,  # Máximo de 4 colunas por linha
        trendline='ols',
        opacity=0.6,
        color_discrete_sequence=['#1f3c88'],
        labels={
            'log_base_price': 'ln(Base Price)',
            'log_effective_price': 'ln(Effective Total Price)',
            'loc': 'NUTS II'
        }
    )

    # Estilo e tamanho do gráfico
    fig.update_traces(marker=dict(size=4))  # Pontos menores

    fig.update_layout(
        title='Log-log relationship between base price and effective total price, segmented by region (NUTS II)',
        template='simple_white',
        height=500,  # Mais pequeno
        margin=dict(t=60, b=40, l=40, r=30),
        font=dict(size=11),
    )

    st.plotly_chart(fig, use_container_width=True)