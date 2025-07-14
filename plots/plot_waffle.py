import plotly.graph_objects as go
import streamlit as st

def plot_waffle(df):
    # Dados e cores
    categories = {
        'Standard Procedure Notice': 86.5,
        'Urgent Tender Notice': 5.7,
        'Deadline Extension Notice': 5.6,
        'Notice Correction Statement': 2.2
    }

    color_map = {
        'Standard Procedure Notice': '#001F3F',
        'Urgent Tender Notice': '#7FDBFF',
        'Deadline Extension Notice': '#FF851B',
        'Notice Correction Statement': '#FFB07C'
    }

    total_squares = 100
    values = [round(v) for v in categories.values()]
    labels = list(categories.keys())

    # Criar vetor com rótulos repetidos
    waffle_data = []
    for label, val in zip(labels, values):
        waffle_data.extend([label] * val)

    # Grid com quadrados pequenos e colados
    n_cols = 10
    n_rows = total_squares // n_cols
    x = [i % n_cols for i in range(total_squares)]
    y = [n_rows - 1 - (i // n_cols) for i in range(total_squares)]
    colors = [color_map[l] for l in waffle_data]

    fig = go.Figure(data=go.Scatter(
        x=x, y=y, mode='markers',
        marker=dict(size=20, color=colors, symbol='square'),
        hovertext=[f"{l}: {categories[l]}%" for l in waffle_data],
        hoverinfo='text'
    ))

    # Legenda desenhada manualmente
    legend_y = 9.5
    spacing = 1.1
    for label in labels:
        fig.add_shape(
            type="rect",
            x0=11, x1=11.5, y0=legend_y - 0.3, y1=legend_y + 0.3,
            fillcolor=color_map[label],
            line=dict(width=0)
        )
        fig.add_annotation(
            x=11.6, y=legend_y,
            text=label,
            showarrow=False,
            font=dict(size=12),
            xanchor="left"
        )
        legend_y -= spacing

    fig.update_layout(
        title="Distribution of Procurement Notice Types",
        title_x=0.0,  # Alinha o título à esquerda
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=380,
        width=750,
        margin=dict(l=10, r=10, t=50, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    st.plotly_chart(fig)