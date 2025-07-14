import plotly.express as px
import pandas as pd
import streamlit as st

def plot_mean_bidders_per_cpv(df):
    if 'CPV_agrupado' not in df.columns or 'bidders' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias.")
        return

    # Agrupamento e ordenação decrescente
    grouped = (
        df.groupby('CPV_agrupado')['bidders']
        .mean()
        .reset_index(name='avg_bidders')
        .sort_values(by='avg_bidders', ascending=False)
    )

    # Definir ordem manual do eixo y com base na ordenação
    grouped['CPV_agrupado'] = pd.Categorical(
        grouped['CPV_agrupado'],
        categories=grouped['CPV_agrupado'],
        ordered=True
    )

    fig = px.bar(
        grouped,
        x='avg_bidders',
        y='CPV_agrupado',
        orientation='h',
        color_discrete_sequence=["#0B2C54"],
        labels={
            'avg_bidders': 'Average Bidders',
            'CPV_agrupado': 'CPV Group'
        }
    )

    fig.update_layout(
        title='Average Number of Bidders per CPV Group',
        title_x=0.0,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="black")
    )

    st.plotly_chart(fig, use_container_width=True)