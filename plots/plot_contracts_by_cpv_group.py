import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import numpy as np
import streamlit as st
import time


def plot_contracts_by_cpv_group(df):
    if 'contract_year' not in df.columns or 'CPV_agrupado' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias.")
        return

    # Contar número de contratos por ano e grupo CPV
    grouped = df.groupby(['contract_year', 'CPV_agrupado']).size().reset_index(name='num_contracts')

    fig = px.line(
        grouped,
        x='contract_year',
        y='num_contracts',
        color='CPV_agrupado',
        markers=True,
        labels={
            'contract_year': 'Contract Year',
            'num_contracts': 'Number of Contracts',
            'CPV_agrupado': 'CPV Group'
        }
    )

    # Calcular e adicionar variação percentual por grupo
    variation_annotations = []
    for group in grouped['CPV_agrupado'].unique():
        sub_df = grouped[grouped['CPV_agrupado'] == group].sort_values('contract_year')
        if len(sub_df) >= 2:
            initial = sub_df.iloc[0]['num_contracts']
            final = sub_df.iloc[-1]['num_contracts']
            if initial > 0:
                variation = ((final - initial) / initial) * 100
                year = sub_df.iloc[-1]['contract_year']
                text = f"{variation:+.1f}%"
                variation_annotations.append(dict(
                    x=year,
                    y=final,
                    text=text,
                    showarrow=False,
                    font=dict(size=11),
                    xanchor='left',
                    yanchor='bottom'
                ))

    fig.update_layout(
        title="Evolution of the Number of Contracts per CPV Group Over Time",
        title_x=0.0,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="black"),
        legend_title_text='CPV Group',
        annotations=variation_annotations
    )

    # Criar key única com timestamp
    unique_key = f"plot_contracts_{int(time.time() * 1000)}"
    st.plotly_chart(fig, use_container_width=True, key=unique_key)