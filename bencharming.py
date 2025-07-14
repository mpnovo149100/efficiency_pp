import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from plotly import graph_objects as go

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)
def apply_benchmark_gap(df, benchmark="p75"):
    df = df.copy()

    quantile_map = {"p50": 0.50, "p75": 0.75, "p90": 0.90}
    if benchmark not in quantile_map:
        raise ValueError("Benchmark must be one of: 'p50', 'p75', 'p90'")

    threshold = df["efficiency"].quantile(quantile_map[benchmark])

    # 🟡 Cálculo sempre baseado no benchmark — independentemente de ser mais ou menos eficiente
    df["price_sim"] = df["effective_total_price"] * (df["efficiency"] / threshold)

    # Gap real vs simulado (agora pode ser negativo)
    df["gap"] = df["effective_total_price"] - df["price_sim"]
    df["gap_pct"] = np.where(
        df["effective_total_price"] > 0,
        (df["gap"] / df["effective_total_price"]) * 100,
        np.nan
    )
    df["gap_sign"] = np.sign(df["gap"])  # <--- agora vai dar positivos e negativos

    return df

def run_benchmark_and_store(df, benchmark='p75'):
    df_bench = apply_benchmark_gap(df, benchmark)
    st.session_state['bench_df'] = df_bench

def show_benchmark_metrics():
    st.markdown("""
**How to Interpret These Indicators:**  
• <b>Average Overspending</b>: average % by which inefficient contracts exceeded expected cost.  
• <b>Contracts Above Benchmark</b>: inefficient contracts (gap > 0).  
• <b>Contracts Below Benchmark</b>: efficient contracts (gap < 0).
""", unsafe_allow_html=True)

    # Benchmark selection
    col_select, _, _, _ = st.columns(4)
    with col_select:
        benchmark_label = st.selectbox("Select Benchmark Scenario:", ["p50", "p75", "p90"], format_func=lambda x: x.upper())

    # Load and process data
    raw_df = load_data("Data/dados_completos.csv")

    if (
        'bench_df' not in st.session_state or
        st.session_state.get('current_benchmark') != benchmark_label
    ):
        run_benchmark_and_store(raw_df, benchmark=benchmark_label)
        st.session_state['current_benchmark'] = benchmark_label

    df = st.session_state['bench_df']

    # KPIs
    avg_overspend = df.loc[df["gap_sign"] > 0, "gap_pct"].mean()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Overspending (%)", f"{avg_overspend:.1f}%")
    with col2:
        st.metric("Contracts Above Benchmark", int((df['gap_sign'] > 0).sum()))
    with col3:
        st.metric("Contracts Below Benchmark", int((df['gap_sign'] < 0).sum()))
    st.markdown("---")
    # Summary
    benchmark_value = df["efficiency"].quantile({"p50": 0.5, "p75": 0.75, "p90": 0.9}[benchmark_label])
    df["price_sim"] = df.apply(
        lambda row: row["effective_total_price"] * (row["efficiency"] / benchmark_value)
        if row["efficiency"] < benchmark_value else row["effective_total_price"],
        axis=1
    )
    real_cost = df["effective_total_price"].sum()
    sim_cost = df["price_sim"].sum()
    savings = real_cost - sim_cost
   
    st.markdown("##### Summary & Estimated Savings")
    col_left, col_right = st.columns(2)

    with col_left:
        summary = pd.DataFrame({
            "Metric": ["Scenario", "Real Cost (€)", "Simulated Cost (€)", "Estimated Savings (€)"],
            "Value": [
                benchmark_label.upper(),
                f"€ {real_cost:,.0f}".replace(",", " "),
                f"€ {sim_cost:,.0f}".replace(",", " "),
                f"€ {savings:,.0f}".replace(",", " ")
            ]
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)

    with col_right:
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute", "relative", "total"],
            x=["Real Cost", "Savings", "Simulated Cost"],
            y=[real_cost, -savings, sim_cost],
            connector={"line": {"color": "#AAB2BD"}},
            decreasing={"marker": {"color": "#2C3E50"}},
            increasing={"marker": {"color": "#E74C3C"}},
            totals={"marker": {"color": "#2980B9"}}
        ))
        fig.update_layout(
            title=f"Estimated Savings Applying {benchmark_label.upper()} Benchmark",
            yaxis_title="€",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    # Filtros
    st.markdown("##### Contracts Above / Below Benchmark by Variable")
    left_col, right_col = st.columns([1, 3])
    with left_col:
        st.markdown("Filters")
        selected_locs = st.multiselect("Select Location(s)", df["loc"].dropna().unique().tolist())
        min_y, max_y = int(df["contract_year"].min()), int(df["contract_year"].max())
        selected_years = st.slider("Select Contract Year Range", min_value=min_y, max_value=max_y, value=(min_y, max_y))

    df_filtered = df[
        df["loc"].isin(selected_locs) &
        df["contract_year"].between(*selected_years)
    ].copy()
    df_filtered["bench_status"] = df_filtered["gap_sign"].map({1: "Above", -1: "Below", 0: "On Target"})

    with right_col:
        pretty_names = {
            'act_type': "Type of Act",
            'base_price': "Base Price",
            'execution_dummy': "Execution Rate",
            'environmental': "Environmental Criteria",
            'contract_year': "Contract Year",
            'covid_pandemic': "Pandemic Period",
            'loc': "Location NUTSII",
            'CPV_agrupado': "CPV Group",
            'bidders': "Number of Bidders"
        }
        selected_var = st.selectbox("Choose variable:", options=list(pretty_names), format_func=lambda x: pretty_names[x])

        if selected_var == "base_price":
            bins = [0, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, float('inf')]
            labels = ["<10K", "10K–50K", "50K–100K", "100K–500K", "500K–1M", "1M–5M", "5M+"]
            df_filtered["bin"] = pd.cut(df_filtered["base_price"], bins=bins, labels=labels)
            x_var = "bin"
        else:
            x_var = selected_var
            if selected_var == "execution_dummy":
                df_filtered[selected_var] = df_filtered[selected_var].map({0: "Not Met", 1: "Met"})

        grouped = df_filtered.groupby([x_var, "bench_status"]).size().reset_index(name="contracts")
        
        fig = px.bar(
            grouped,
            x=x_var, y="contracts",
            color="bench_status",
            barmode="group",
            color_discrete_map={"Above": "#E74C3C", "Below": "#3498DB", "On Target": "#BDC3C7"},
            labels={"contracts": "Number of Contracts", x_var: pretty_names.get(selected_var, selected_var)}
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="black"))
        st.plotly_chart(fig, use_container_width=True)
