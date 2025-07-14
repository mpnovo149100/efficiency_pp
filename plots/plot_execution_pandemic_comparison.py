import plotly.express as px
import pandas as pd
import streamlit as st

def plot_execution_pandemic_comparison(df: pd.DataFrame):
    """
    Figure 4.15: Execution rate during pandemic and non-pandemic periods.
    """
    if 'covid_pandemic' not in df.columns or 'execution_dummy' not in df.columns:
        st.warning("Required columns: 'covid_pandemic' and 'execution_dummy'.")
        return

    # Mapeamento para nomes legíveis
    df_filtered = df[['covid_pandemic', 'execution_dummy']].dropna()
    df_filtered['Pandemic Period'] = df_filtered['covid_pandemic'].map({1: 'Pandemic', 0: 'Non–Pandemic'})
    df_filtered['Execution'] = df_filtered['execution_dummy'].map({1: 'Met', 0: 'Not Met'})

    # Agrupar e calcular percentagens
    grouped = (
        df_filtered
        .groupby(['Pandemic Period', 'Execution'])
        .size()
        .reset_index(name='Count')
    )
    totals = grouped.groupby('Pandemic Period')['Count'].transform('sum')
    grouped['Percentage'] = grouped['Count'] / totals

    # Gráfico
    fig = px.bar(
        grouped,
        x='Pandemic Period',
        y='Percentage',
        color='Execution',
        barmode='stack',
        color_discrete_map={
            'Met': '#1f3c88',
            'Not Met': '#bcbcbc'
        },
        labels={
            'Percentage': 'Execution Compliance Rate',
            'Pandemic Period': 'Pandemic Period'
        },
        title="Execution Rate During Pandemic and Non-Pandemic Periods"
    )

    fig.update_layout(
        yaxis_tickformat='.0%',
        yaxis_title="Execution Compliance Rate",
        xaxis_title="Pandemic Period",
        legend_title="Execution",
        template="simple_white",
        margin=dict(l=40, r=30, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)