import plotly.express as px
import pandas as pd
import streamlit as st

def plot_density_ln_effective_price_by_environmental(df: pd.DataFrame):
    df = df.copy()

    # Garantir colunas válidas e sem NaN
    df = df.dropna(subset=['ln_effective_total_price', 'environmental'])

    # Mapeamento mais amigável
    df['Environmental Criteria'] = df['environmental'].map({
        0: 'No Criteria',
        1: 'Criteria'
    })

    fig = px.histogram(
        df,
        x='ln_effective_total_price',
        color='Environmental Criteria',
        histnorm='density',
        barmode='overlay',
        opacity=0.5,
        color_discrete_map={
            'No Criteria': '#bcbcbc',
            'Criteria': '#1f3c88'
        },
        labels={
            'ln_effective_total_price': 'Logₑ(Effective Price)',
            'Environmental Criteria': 'Environmental'
        },
        title="Density of Log(Effective Price) by Environmental Criteria"
    )

    fig.update_layout(
        xaxis_title='Logₑ(Effective Price)',
        yaxis_title='Density',
        legend_title='Environmental Criteria',
        template='simple_white',
        margin=dict(l=40, r=30, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)