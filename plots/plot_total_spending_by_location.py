import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 
import statsmodels.api as sm

def plot_total_spending_by_location(df: pd.DataFrame):
    """
    Figure 4.20: Total spending by location (NUTS II), based on the effective total price.
    """
    if 'loc' not in df.columns or 'effective_total_price' not in df.columns:
        st.warning("Colunas necessárias ('location' ou 'effective_total_price') não encontradas na base de dados.")
        return

    df_plot = df.copy()
    df_plot = df_plot[df_plot['loc'].notna()]
    df_plot = df_plot[df_plot['effective_total_price'].notna()]

    df_grouped = df_plot.groupby('loc', as_index=False)['effective_total_price'].sum()
    df_grouped = df_grouped.rename(columns={
        'loc': 'Location (NUTS II)',
        'effective_total_price': 'Total Spending'
    }).sort_values('Total Spending', ascending=False)

    fig = px.bar(
        df_grouped,
        x='Location (NUTS II)',
        y='Total Spending',
        text='Total Spending',
        labels={'Total Spending': 'Total Spending (€)'},
        color_discrete_sequence=['#1f3c88']
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        title="Total Spending by Location (NUTS II)",
        template="simple_white",
        xaxis_title="Location (NUTS II)",
        yaxis_title="Total Spending (€)",
    )

    st.plotly_chart(fig, use_container_width=True)
