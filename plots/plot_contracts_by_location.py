import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 
import statsmodels.api as sm


def plot_contracts_by_location(df: pd.DataFrame):
    """
    Figure 4.19: Number of contracts by location (NUTS II).
    """
    if 'loc' not in df.columns:
        st.warning("Coluna 'location' não encontrada na base de dados.")
        return

    df_plot = df.copy()
    df_plot = df_plot[df_plot['loc'].notna()]
    df_counts = df_plot['loc'].value_counts().reset_index()
    df_counts.columns = ['Location (NUTS II)', 'Number of Contracts']

    fig = px.bar(
        df_counts,
        x='Location (NUTS II)',
        y='Number of Contracts',
        text='Number of Contracts',
        labels={
            'loc': 'Location (NUTS II)',
            'Number of Contracts': 'Number of Contracts'
        },
        color_discrete_sequence=['#1f3c88']
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        title="Number of Contracts by Location (NUTS II)",
        template="simple_white",
        xaxis_title="Location (NUTS II)",
        yaxis_title="Number of Contracts"
    )

    st.plotly_chart(fig, use_container_width=True)

