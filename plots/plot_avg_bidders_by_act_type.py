import plotly.graph_objects as go
import streamlit as st

def plot_avg_bidders_by_act_type(df):
    if 'act_type' not in df.columns or 'bidders' not in df.columns:
        st.warning("As colunas 'act_type' ou 'bidders' não existem no DataFrame.")
        return
    
    # Cálculo da média de concorrentes por tipo de anúncio
    avg_bidders = df.groupby('act_type')['bidders'].mean().round(1)
    avg_bidders = avg_bidders.sort_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=avg_bidders.index.astype(str),
        y=avg_bidders.values,
        marker_color="#0B2C54",
        hovertemplate='%{x}: %{y:.1f}<extra></extra>',
        text=None  # <- esta linha garante que nada é exibido no topo das barras
    ))

    fig.update_layout(
        title="Average Number of Bidders by Procurement Notice Type",
        xaxis_title="Notice Type",
        yaxis_title="Average Number of Bidders",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(range=[0, max(avg_bidders.values)*1.2])
    )

    st.plotly_chart(fig, use_container_width=True)