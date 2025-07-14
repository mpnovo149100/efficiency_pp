import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 
import statsmodels.api as sm


def plot_bidders_vs_log_price_pandemic(df: pd.DataFrame):
    """
    Figure 4.18: Relationship between number of bidders and log effective price,
    colored by pandemic period.
    """
    if 'bidders' not in df.columns or 'effective_total_price' not in df.columns or 'covid_pandemic' not in df.columns:
        st.warning("Colunas necessárias: 'bidders', 'effective_total_price', 'covid_pandemic'.")
        return

    df_plot = df.copy()
    df_plot = df_plot[df_plot['effective_total_price'] > 0]
    df_plot['log_effective_price'] = np.log(df_plot['effective_total_price'])
    df_plot['Pandemic Period'] = df_plot['covid_pandemic'].map({0: 'Non–Pandemic', 1: 'Pandemic'})

    fig = px.scatter(
        df_plot,
        x='bidders',
        y='log_effective_price',
        color='Pandemic Period',
        opacity=0.6,
        labels={
            'bidders': 'Number of Bidders',
            'log_effective_price': 'Log of Effective Price'
        },
        color_discrete_map={
            'Non–Pandemic': '#A9A9A9',
            'Pandemic': '#FFA500'
        }
    )

    fig.update_layout(
        title="Relationship Between Number of Bidders and Log(Effective Price) by Pandemic Period",
        template="simple_white"
    )

    st.plotly_chart(fig, use_container_width=True)
