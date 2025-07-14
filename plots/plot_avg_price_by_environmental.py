import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import numpy as np 



def plot_avg_price_by_environmental(df):
    if 'contract_year' not in df.columns or 'environmental' not in df.columns or 'effective_total_price' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias.")
        return

    # Agrupar por ano e critério ambiental
    grouped = df.groupby(['contract_year', 'environmental'])['effective_total_price'].mean().reset_index()

    # Mapear rótulos para a legenda
    grouped['Environmental Criteria'] = grouped['environmental'].map({0: 'No Environmental', 1: 'With Environmental'})

    fig = px.line(
        grouped,
        x='contract_year',
        y='effective_total_price',
        color='Environmental Criteria',
        markers=True,
        labels={
            'contract_year': 'Contract Year',
            'effective_total_price': 'Average Price'
        },
        color_discrete_map={
            'No Environmental': 'gray',
            'With Environmental': 'darkblue'
        }
    )

    fig.update_layout(
        title="Average Final Effective Price by Environmental Criteria",
        title_x=0.0,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="black"),
        legend_title_text='Environmental Criteria'
    )

    st.plotly_chart(fig, use_container_width=True)
