import pandas as pd
import plotly.express as px
import streamlit as st

def show_rf_cost_mitigation_dashboard():
    st.set_page_config(layout="wide")
    
    threshold = 0.065  # Risk threshold from Youden J metric

    pretty_variable_names = {
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

    @st.cache_data
    def load_data():
        return pd.read_csv("Data/dados.csv")

    @st.cache_data
    def load_shap_values():
        try:
            df_shap = pd.read_csv("Data/shap_values.csv")
            required_cols = [
                "variable", "contribution", "variable_name", "variable_value", "sign", "label"
            ]
            if not all(col in df_shap.columns for col in required_cols):
                missing = [col for col in required_cols if col not in df_shap.columns]
                st.error(f"Invalid shap_values.csv file. Missing columns: {missing}")
                return None
            return df_shap
        except FileNotFoundError:
            st.error("File shap_values.csv not found.")
            return None
        except Exception as e:
            st.error(f"Error loading shap_values.csv: {e}")
            return None

    df = load_data()
    df_shap = load_shap_values()

    expected_cols = ["effective_total_price", "risk_prob", "price_sim_rf", "custo_aumentou"]
    if not all(col in df.columns for col in expected_cols):
        st.error(f"File 'Data/dados.csv' must contain: {expected_cols}")
        return

    # Simulated cost with substitution of high-risk contracts
    sim_cost_high = df.loc[df["risk_prob"] >= threshold, "price_sim_rf"].sum()
    sim_cost_safe = df.loc[df["risk_prob"] < threshold, "effective_total_price"].sum()
    simulated_cost = sim_cost_high + sim_cost_safe
    real_cost = df["effective_total_price"].sum()
    savings = real_cost - simulated_cost

    # KPIs
    pct_increase = (df["custo_aumentou"] == 1).mean() * 100
    pct_risk = (df["risk_prob"] >= threshold).mean() * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Real Increases", f"{pct_increase:.2f}%")
    col2.metric("Contracts at Risk", f"{pct_risk:.2f}%")
    col3.metric("Estimated Savings", f"€ {savings:,.0f}".replace(",", " "))

    st.markdown("---")

    # Distribution
    st.markdown("### Distribution of Cost Increase Risk")
    df["Outcome Label"] = df["custo_aumentou"].map({0: "No Increase", 1: "Increase"})
    fig = px.histogram(
    df,
    x="risk_prob",
    color="Outcome Label",
    nbins=40,
    barmode="overlay",
    histnorm="percent",
    color_discrete_map={
        "No Increase": "#bcbcbc",  # cinzento claro
        "Increase": "#0B2C54"      # azul escuro
    },
    labels={
        "risk_prob": "Cost Increase Probability",
        "Outcome Label": "Observed Outcome"
    }
)
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="black"),
        legend_title_text="Observed Outcome"
    )
    st.markdown("""
**Note:**  
- **"No Increase" (0)** indicates contracts where the final price did **not** increase.  
- **"Increase" (1)** indicates contracts where the final price was **higher** than expected.
""")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # Top 20 Contracts at Risk
    st.markdown("### Top 20 Contracts with Highest Risk")
    cols_to_show = [
        "nipcs", "Location", "contract_year", "CPV_agrupado", "act_type",
        "bidders", "efficiency", "effective_total_price", "risk_prob"
    ]
    if all(col in df.columns for col in cols_to_show):
        top_risk = df[df["risk_prob"] >= threshold].sort_values("risk_prob", ascending=False)
        df_top20 = top_risk[cols_to_show].head(20).copy()
        df_top20["risk_prob"] = (df_top20["risk_prob"] * 100).round(2).astype(str) + "%"
        df_top20["efficiency"] = (df_top20["efficiency"] * 100).round(2).astype(str) + "%"
        st.dataframe(df_top20, use_container_width=True)

    st.markdown("---")

    # Average Risk by Group
    st.markdown("### Average Risk by Group")
    var = st.selectbox(
        "Select a variable:",
        options=list(pretty_variable_names.keys()),
        format_func=lambda x: pretty_variable_names.get(x, x)
    )

    if var in df.columns:
        group_risk = df.groupby(var)["risk_prob"].mean().reset_index()
        group_risk["risk_prob"] = group_risk["risk_prob"] * 100
        var_pretty = pretty_variable_names.get(var, var)

        fig_group = px.bar(
            group_risk,
            x=var,
            y="risk_prob",
            labels={var: var_pretty, "risk_prob": "Average Risk (%)"},
            color_discrete_sequence=["#0B2C54"]
        )
        fig_group.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="black")
        )
        st.plotly_chart(fig_group, use_container_width=True)
  
    st.markdown("#### Key insights from top-risk contracts")
    st.markdown(
        """
**Hot-spots**

- 70 % of the top-risk contracts are in **Lisboa (PT170)**.
- 13 / 20 belong to **Services – Standard Procedure Notice**.
- Buyer **NIPCS 509 540 716** alone accounts for 3 of the 5 riskiest awards.

**Efficiency signal**

Low technical efficiency (< 40 %) aligns with risk > 60 %.

**Recommended actions**

1. Audit NIPCS 506 361 438 ( Instituto Português de Oncologia de Coimbra Francisco Gentil E.p.e) & 509 540 716 (Spms - Serviços Partilhados do Ministério da Saúde, E.p.e).
2. Add pre-award quality checks for Standard Procedures in Service contracts.
3. Encourage > 2 qualified bidders per tender to curb under-bidding.
"""
    )
    st.markdown("---")

    # SHAP Variable Importance
    if df_shap is not None:
        st.markdown("### SHAP: Variable Importance")

        shap_mean = (
            df_shap.groupby("variable_name")["contribution"].mean()
            .abs().sort_values(ascending=False).reset_index()
        )

        c1, c2 = st.columns([3, 2])

        with c1:
            fig_shap = px.bar(
                shap_mean,
                x="contribution",
                y="variable_name",
                orientation="h",
                labels={"contribution": "Mean |SHAP|", "variable_name": "Variable"},
                color_discrete_sequence=["#0B2C54"],
                height=450
            )
            fig_shap.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font_color="black",
                yaxis_title="",
                margin=dict(l=30, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_shap, use_container_width=True)

        with c2:
            top3 = shap_mean.head(3)
            bullets = "\n".join(
                f"- **{row.variable_name}** → {row.contribution:.3f}"
                for _, row in top3.iterrows()
            )
            st.markdown(
                f"""
**Key take-aways (top 3 drivers)**  
{bullets}

*Greater absolute SHAP ⇒ stronger impact on predicted cost increase probability.*  
Targeting these drivers in policy or contract design is likely to yield the
largest reduction in risk.
""",
                unsafe_allow_html=False
            )

    st.markdown("---")

    # Real vs Simulated Cost with Savings
    st.markdown("### Estimated Savings Applying Benchmark Strategy")
    col1, col2 = st.columns([3, 2])

    with col1:
        df_cost = pd.DataFrame({
            "Cost Type": ["Real", "Simulated", "Savings"],
            "Value (€)": [real_cost, simulated_cost, savings]
        })

        fig_cost = px.bar(
            df_cost,
            x="Cost Type",
            y="Value (€)",
            text="Value (€)",
            color="Cost Type",
            color_discrete_map={
                "Real": "#0B2C54",
                "Simulated": "#bcbcbc",
                "Savings": "#1f77b4"
            },
            height=420,
            category_orders={"Cost Type": ["Real", "Simulated", "Savings"]}
        )

        fig_cost.update_traces(
            texttemplate='%{text:,}',
            textposition='outside'
        )

        fig_cost.update_layout(
            showlegend=False,
            yaxis_title="Value (€)",
            xaxis_title="",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="black"),
            margin=dict(t=40, r=10, l=10, b=10)
        )

        st.plotly_chart(fig_cost, use_container_width=True)

    with col2:
        st.markdown("#### Key Insights")
        st.markdown(f"""
- **Estimated savings** of approximately **€{int(savings):,}** if high-risk contracts are replaced with cost-efficient alternatives.  
- Only **{pct_risk:.2f}% of contracts** are flagged as high risk, but they **disproportionately drive up total cost**.  
- **Predictive benchmarks** such as P50 from SFA can serve as filters to **automatically flag inefficient allocations**.  
- This approach supports **data-driven cost containment** and **pre-award risk screening** in procurement.
""")

    st.info("⚠️ These are predictive simulations. Application must consider institutional and contractual context.")