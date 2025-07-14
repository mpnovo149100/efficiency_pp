import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st

BLUE = "#0B2C54"

def plot_effective_price_trend(df):
    df = df.copy()
    df = df.dropna(subset=['ln_effective_total_price', 'contract_year'])

    # LOWESS smoothing
    smoothed = sm.nonparametric.lowess(
        df['ln_effective_total_price'],
        df['contract_year'],
        frac=0.3
    )
    smooth_x = [x[0] for x in smoothed]
    smooth_y = [x[1] for x in smoothed]

    # Scatter plot (sem título aqui!)
    fig = px.scatter(
        df,
        x='contract_year',
        y='ln_effective_total_price',
        opacity=0.5,
        color_discrete_sequence=[BLUE],
        labels={
            'contract_year': 'Contract Year',
            'ln_effective_total_price': 'Logₑ(Total Effective Price)'
        }
    )

    # LOWESS line
    fig.add_trace(go.Scatter(
        x=smooth_x,
        y=smooth_y,
        mode='lines',
        name='LOWESS Trend',
        line=dict(color=BLUE, width=3)
    ))

    # Layout (título com cor e alinhamento)
    fig.update_layout(
        title_text="Trend of Log(Effective Price) over Time",
        title_font=dict(color='black', size=20),
        title_x=0.0,
        font=dict(color='black'),
        xaxis=dict(
            title="Contract Year",
            color='white',
            showgrid=False
        ),
        yaxis=dict(
            title="Logₑ(Total Effective Price)",
            color='white',
            showgrid=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)