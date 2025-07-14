import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_execution_by_act_type(df):
    if {'act_type', 'execution_dummy'} - set(df.columns):
        st.warning("Columns 'act_type' and/or 'execution_dummy' missing.")
        return

    # Mapping original labels to numeric codes
    label_map = {
        "Deadline Extension Notice": "1",
        "Notice Correction Statement": "2",
        "Standard Procedure Notice": "3",
        "Urgent Tender Notice": "4"
    }
    label_legend = {
        "1": "Deadline Extension Notice",
        "2": "Notice Correction Statement",
        "3": "Standard Procedure Notice",
        "4": "Urgent Tender Notice"
    }
    df['label_code'] = df['act_type'].map(label_map).fillna("Other")

    exec_counts = (
        df.groupby(['label_code', 'execution_dummy'])
          .size()
          .unstack(fill_value=0)
    )

    for col in [0, 1]:
        exec_counts[col] = exec_counts.get(col, 0)
    exec_perc = exec_counts.div(exec_counts.sum(axis=1), axis=0) * 100
    exec_perc = exec_perc.sort_index()

    fig = go.Figure()
    fig.add_bar(
        x=exec_perc.index,
        y=exec_perc[0],
        name="Not Met",
        marker_color="#001f3f",
        hovertemplate='Code %{x}<br>%{y:.1f}%<extra></extra>'
    )
    fig.add_bar(
        x=exec_perc.index,
        y=exec_perc[1],
        name="Met",
        marker_color="#B0B0B0",
        hovertemplate='Code %{x}<br>%{y:.1f}%<extra></extra>'
    )

    fig.update_layout(
        barmode='stack',
        title="Execution Rate by Procurement Notice Type",
        xaxis_title="Notice Type Code",
        yaxis_title="Execution Rate (%)",
        yaxis=dict(range=[0, 100]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=12),
        legend=dict(orientation="h", y=-0.25, x=0.3),  # legenda embaixo
        margin=dict(t=60, l=60, r=40, b=100)
    )

    fig.update_xaxes(
        tickangle=0,
        tickfont=dict(size=12),
        automargin=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Legenda explicativa abaixo
    st.markdown("**Legend for Notice Type Codes:**")
    for code, desc in label_legend.items():
        st.markdown(f"**{code}** – {desc}")