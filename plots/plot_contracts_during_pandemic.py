import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 
import statsmodels.api as sm


def plot_contracts_during_pandemic(df: pd.DataFrame):
    """
    Figure 4.16: Number of contracts per year during the COVID-19 pandemic period.
    """
    if 'contract_year' not in df.columns or 'covid_pandemic' not in df.columns:
        st.warning("Colunas necessárias: 'contract_year' e 'covid_pandemic'.")
        return

    # Filtrar apenas anos de pandemia
    pandemic_years = df[df['covid_pandemic'] == 1]
    df_grouped = (
        pandemic_years
        .groupby('contract_year')
        .size()
        .reset_index(name='Number of Contracts')
    )

    # Gráfico de linhas com pontos
    fig = px.line(
        df_grouped,
        x='contract_year',
        y='Number of Contracts',
        markers=True,
        labels={
            'contract_year': 'Contract Year',
            'Number of Contracts': 'Number of Contracts'
        }
    )

    fig.update_traces(line_color='#1f3c88', marker=dict(size=8, color='#1f3c88'))
    fig.update_layout(
        title="Number of Contracts During the COVID-19 Pandemic Period",
        xaxis=dict(dtick=1),
        yaxis_title="Number of Contracts",
        template="simple_white",
        margin=dict(l=40, r=30, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)
