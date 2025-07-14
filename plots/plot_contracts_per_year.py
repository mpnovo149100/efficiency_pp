import plotly.graph_objects as go
import statsmodels.api as sm
import pandas as pd
import streamlit as st


def plot_contracts_per_year(df):
    if 'contract_year' not in df.columns:
        st.warning("A coluna 'contract_year' não existe no DataFrame.")
        return

    # Contagem de contratos por ano
    year_counts = df['contract_year'].value_counts().sort_index()
    years = year_counts.index.tolist()
    counts = year_counts.values

    # LOWESS para suavizar tendência
    lowess = sm.nonparametric.lowess
    smoothed = lowess(counts, years, frac=0.3)
    smooth_x = [x[0] for x in smoothed]
    smooth_y = [x[1] for x in smoothed]

    # Calcular variação percentual ano a ano
    pct_change = pd.Series(smooth_y).pct_change() * 100
    pct_text = [""] + [f"{pct:.1f}%" for pct in pct_change[1:]]

    fig = go.Figure()

    # Barras com número de contratos
    fig.add_trace(go.Bar(
        x=years,
        y=counts,
        name="Number of Contracts",
        marker_color="#0B2C54"
    ))

    # Linha de tendência com texto hover de % variação
    fig.add_trace(go.Scatter(
        x=smooth_x,
        y=smooth_y,
        mode='lines+markers',
        name='Trendline (LOWESS)',
        text=pct_text,
        hovertemplate="Year: %{x}<br>Trend: %{y:.0f}<br>Δ YoY: %{text}<extra></extra>",
        line=dict(color='lightgray', width=2),
        marker=dict(color='gray', size=6)
    ))

    fig.update_layout(
        title="Number of Contracts per Year with Trendline and % Change",
        xaxis_title="Contract Year",
        yaxis_title="Number of Contracts",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color="black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig, use_container_width=True)