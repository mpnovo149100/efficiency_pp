import plotly.graph_objects as go
import streamlit as st

def plot_avg_effective_price_by_act_type(df):
    if 'act_type' not in df.columns or 'effective_total_price' not in df.columns:
        st.warning("As colunas 'act_type' ou 'effective_total_price' não existem no DataFrame.")
        return
   
    # Média do preço efetivo por tipo de anúncio
    avg_price = df.groupby('act_type')['effective_total_price'].mean().round(0)
    avg_price = avg_price.sort_index()

    # Formatar com espaço como separador de milhar
    formatted_text = [f"{int(val):,}".replace(",", " ") for val in avg_price.values]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=avg_price.index.astype(str),  # sem chavetas
        y=avg_price.values,
        text=formatted_text,
        textposition="outside",
        marker_color="#0B2C54",
        hovertemplate='<b>%{x}</b><br>€ %{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title="Average Effective Price by Type of Procurement Announcement",
        xaxis_title="Notice Type",
        yaxis_title="Average Effective Price (€)",
        font=dict(color="black"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(range=[0, avg_price.max() * 1.2])
    )

    st.plotly_chart(fig, use_container_width=True)