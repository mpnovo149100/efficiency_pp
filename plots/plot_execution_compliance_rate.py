import plotly.express as px
import pandas as pd
import streamlit as st

def plot_execution_compliance_rate(df: pd.DataFrame):
    """
    Figure 4.14: Stacked bar chart showing the annual execution compliance rate.
    """
    if 'contract_year' not in df.columns or 'execution_dummy' not in df.columns:
        st.warning("Missing columns: 'contract_year' and 'execution_dummy'.")
        return

    # Preparar dados
    df_filtered = df[['contract_year', 'execution_dummy']].dropna()
    df_filtered['Execution'] = df_filtered['execution_dummy'].map({1: 'Met', 0: 'Not Met'})

    # Agrupar e calcular percentagens
    grouped = df_filtered.groupby(['contract_year', 'Execution']).size().reset_index(name='Count')
    totals = grouped.groupby('contract_year')['Count'].transform('sum')
    grouped['Percentage'] = grouped['Count'] / totals

    # Gráfico
    fig = px.bar(
        grouped,
        x='contract_year',
        y='Percentage',
        color='Execution',
        barmode='stack',
        color_discrete_map={
            'Met': '#1f3c88',       # Azul escuro
            'Not Met': '#bcbcbc'    # Cinza
        },
        labels={
            'contract_year': 'Contract Year',
            'Percentage': 'Execution Compliance Rate',
            'Execution': 'Execution'
        },
        title="Annual Execution Compliance Rate by Contract Year"
    )

    fig.update_layout(
        yaxis_tickformat='.0%',  # mostrar percentagens
        yaxis_title="Execution Compliance Rate",
        xaxis_title="Contract Year",
        legend_title="Execution",
        template="simple_white",
        margin=dict(l=40, r=30, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)