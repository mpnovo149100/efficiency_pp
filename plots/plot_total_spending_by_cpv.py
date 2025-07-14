import plotly.express as px
import pandas as pd
import streamlit as st

def plot_total_spending_by_cpv(df):
    if 'CPV_agrupado' not in df.columns or 'effective_total_price' not in df.columns:
        st.warning("O DataFrame não contém as colunas necessárias.")
        return

    # Soma da despesa por grupo CPV
    spending = (
        df.groupby('CPV_agrupado')['effective_total_price']
        .sum()
        .reset_index(name='total_spending')
        .sort_values('total_spending', ascending=False)
    )

    # Manter ordem
    spending['CPV_agrupado'] = pd.Categorical(
        spending['CPV_agrupado'],
        categories=spending['CPV_agrupado'],
        ordered=True
    )

    # Coluna dummy para forçar a cor
    spending['cor'] = 'All'

    fig = px.bar(
        spending,
        x='total_spending',
        y='CPV_agrupado',
        orientation='h',
        color='cor',
        color_discrete_map={'All': '#0B2C54'},
        labels={
            'total_spending': 'Total Spending',
            'CPV_agrupado': 'CPV Group'
        }
    )

    fig.update_layout(
        title="Total Expenditure per CPV Group Across All Contracts",
        title_x=0.0,  # à esquerda
        title_font=dict(color="#0B2C54", size=18),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="black")
    )

    st.plotly_chart(fig, use_container_width=True)