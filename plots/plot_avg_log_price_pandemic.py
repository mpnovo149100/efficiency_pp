import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 
import statsmodels.api as sm


def plot_avg_log_price_pandemic(df: pd.DataFrame):
    """
    Figure 4.17: Average log effective price during and outside the pandemic period.
    """
    if 'effective_total_price' not in df.columns or 'covid_pandemic' not in df.columns:
        st.warning("Colunas necessárias: 'effective_total_price' e 'covid_pandemic'.")
        return

    df_plot = df.copy()
    df_plot = df_plot[df_plot['effective_total_price'] > 0]  # evitar log(0)
    df_plot['log_price'] = np.log(df_plot['effective_total_price'])

    df_plot['Pandemic Period'] = df_plot['covid_pandemic'].map({0: 'Non–Pandemic', 1: 'Pandemic'})

    df_grouped = df_plot.groupby('Pandemic Period')['log_price'].mean().reset_index()

    fig = px.bar(
        df_grouped,
        x='Pandemic Period',
        y='log_price',
        labels={'log_price': 'Average Log Price'},
        color='Pandemic Period',
        color_discrete_sequence=['#A9A9A9', '#1f3c88']
    )

    fig.update_layout(
        title="Average Log Effective Price: Pandemic vs Non-Pandemic",
        yaxis_title="Average Log Price",
        xaxis_title="Pandemic Period",
        showlegend=False,
        template="simple_white"
    )

    st.plotly_chart(fig, use_container_width=True)
