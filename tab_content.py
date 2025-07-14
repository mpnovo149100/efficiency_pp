import streamlit as st
from utils import *
import pandas as pd
from plot_registy import plot_registry
import plotly.express as px
from bencharming import *
from sfa import show_efficiency_dashboard

pretty_variable_names = {
        'act_type': "Type of Act",
        'base_price': "Base Price",
        'execution_dummy': "Execution Rate",
        'effective_total_price': "Effective Total Price",
        'environmental': "Environmental Criteria",
        'contract_year': "Contract Year",
        'covid_pandemic': "Pandemic Period ",
        'loc': "Location NUTSII",
        'CPV_agrupado': "CPV Group",
        'bidders': "Number of Bidders"
    }

def run_benchmark_and_store(df, benchmark='p75'):
    df_bench = apply_benchmark_gap(df, benchmark)
    st.session_state['bench_df'] = df_bench

def _to_ts(value):
    """Aceita datetime.date, pd.Timestamp ou str e devolve pd.Timestamp."""
    return pd.to_datetime(value)

# ──────────────────────────────────────────────
#  Callbacks dos date_inputs
# ──────────────────────────────────────────────
def update_initial_date():
    sel_init = _to_ts(st.session_state["initial_date_input"])
    sel_final = _to_ts(st.session_state["final_date"])

    # Se a nova data inicial for > data final, ajusta a final
    if sel_init > sel_final:
        st.session_state["final_date"]       = sel_init
        st.session_state["final_date_input"] = sel_init.date()

    st.session_state["initial_date"] = sel_init

def update_final_date():
    sel_final = _to_ts(st.session_state["final_date_input"])
    sel_init  = _to_ts(st.session_state["initial_date"])

    # Se a nova data final for < data inicial, ajusta a inicial
    if sel_final < sel_init:
        st.session_state["initial_date"]       = sel_final
        st.session_state["initial_date_input"] = sel_final.date()

    st.session_state["final_date"] = sel_final

def new_dashboard_tab():
    date_columns = st.columns([1, 1, 2, 3])
    kpi_columns = st.columns([2, 2, 2, 2], gap="medium")

    file_path = "Data/dados_completos.csv"
    df = pd.DataFrame(load_data(file_path))

    # Datas
    df['contract_date'] = pd.to_datetime(df['contract_date'], errors='coerce')
    df['contract_close_date'] = pd.to_datetime(df['contract_close_date'], errors='coerce')

    # Inicializa session_state com base no FECHO do contrato
    oldest_date = df['contract_close_date'].min()
    newest_date = df['contract_close_date'].max()
    
    if 'initial_date' not in st.session_state:
        st.session_state['initial_date'] = oldest_date
    if 'final_date' not in st.session_state:
        st.session_state['final_date'] = newest_date

    # Date Inputs
    with date_columns[0]:
        st.date_input(
            label="Initial Close Date",
            value=st.session_state['initial_date'].date(),
            min_value=oldest_date.date(),
            max_value=newest_date.date(),
            key='initial_date_input',
            on_change=update_initial_date
        )

    with date_columns[1]:
        st.date_input(
            label="Final Close Date",
            value=st.session_state['final_date'].date(),
            min_value=oldest_date.date(),
            max_value=newest_date.date(),
            key='final_date_input',
            on_change=update_final_date
        )

    # Atribuir as datas filtradas
    initial = pd.to_datetime(st.session_state['initial_date_input'])
    final = pd.to_datetime(st.session_state['final_date_input'])

    # ✅ Filtro do DataFrame com base no FECHO do contrato
    filtered_df = df[
        (df['contract_close_date'] >= initial) &
        (df['contract_close_date'] <= final)
    ]

    # Duração do contrato
    df['Contract_Duration_Days'] = (df['contract_close_date'] - df['contract_date']).dt.days
    df['Contract_Duration_Days'] = df['Contract_Duration_Days'].astype('Int64')

    # Formato string para exibição
    df['contract_close_date_str'] = df['contract_close_date'].dt.strftime('%d-%m-%Y')
    df['contract_date_str'] = df['contract_date'].dt.strftime('%d-%m-%Y')
    with date_columns[2]:
        # Filter available variables
        available_pretty_vars = {
            var: name for var, name in pretty_variable_names.items() if var in df.columns
        }

        # Create dropdown with pretty names
        selected_pretty_name = st.selectbox("Select Variable", list(available_pretty_vars.values()))

        # Find corresponding technical name
        selected_variables = [k for k, v in available_pretty_vars.items() if v == selected_pretty_name][0]
        
       
    
    with kpi_columns[0]:
        total_contracts = len(filtered_df)
        st.metric("# Closed Contracts", f"{total_contracts}")

    with kpi_columns[1]:
        st.metric("Average Efficiency", "20.9%")

    with kpi_columns[2]:
        st.metric("Achieved Contracts", "58.2%")
        var = selected_variables  # apenas uma variável selecionada no st.selectbox

    st.markdown("---") 

    # ------------------------------------------------------------------
    # 3)  RENDER SECTION  –  inside new_dashboard_tab
    # ------------------------------------------------------------------
    # …
    
    if selected_variables in plot_registry:
       

        for i, plot_info in enumerate(plot_registry[selected_variables]):
            if i > 0:
                st.markdown("---")

            col1, col2 = st.columns([2, 1])

            with col1:
               
                plot_info['func'](filtered_df)  # <- aqui é o ponto importante

            with col2:
                st.markdown("**Insight**")
                st.markdown(plot_info['insight'])

def show_benchmark_metrics():
    # Explicação
    st.markdown("""
<small>
**How to Interpret These Indicators:**  
• <b>Average Overspending</b>: the average percentage by which contracts exceed the expected cost based on the selected benchmark.  
• <b>Contracts Above Benchmark</b>: number of contracts performing below the benchmark (higher than expected costs).  
• <b>Contracts Below Benchmark</b>: number of contracts performing above the benchmark (more efficient than expected).
</small>
""", unsafe_allow_html=True)

    # Selecionar cenário
    col_select, _, _, _ = st.columns(4)
    with col_select:
        benchmark_label = st.selectbox(
            "Select Benchmark Scenario:",
            options=["p50", "p75", "p90"],
            format_func=lambda x: x.upper()
        )

    # Verifica se benchmark já foi calculado
    file_path = "Data/dados_completos.csv"
    raw_df = pd.DataFrame(load_data(file_path))

    if (
        'bench_df' not in st.session_state or
        st.session_state.get('current_benchmark') != benchmark_label
    ):
        run_benchmark_and_store(raw_df, benchmark=benchmark_label)
        st.session_state['current_benchmark'] = benchmark_label

    # Carrega df já com gap, simulação, etc.
    df = st.session_state['bench_df']

    # KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Overspending (%)", f"{df['gap_pct'].mean():.1f}%")
    with col2:
        st.metric("Contracts Above Benchmark", int((df['gap_sign'] > 0).sum()))
    with col3:
        st.metric("Contracts Below Benchmark", int((df['gap_sign'] < 0).sum()))

    st.write("Explore potential savings by simulating efficiency improvements across contracts.")

    # Simulação de custos
    if 'efficiency' not in df.columns or 'effective_total_price' not in df.columns:
        st.warning("Missing required columns: 'efficiency' and 'effective_total_price'.")
        return

    quantile_map = {"p50": 0.5, "p75": 0.75, "p90": 0.9}
    benchmark_value = df['efficiency'].quantile(quantile_map[benchmark_label])

    df["price_sim"] = df.apply(
        lambda row: row['effective_total_price'] * (row['efficiency'] / benchmark_value)
        if row['efficiency'] < benchmark_value else row['effective_total_price'],
        axis=1
    )

    real_cost = df['effective_total_price'].sum()
    sim_cost = df['price_sim'].sum()
    savings = real_cost - sim_cost

    st.markdown("#### 💰 Summary & Estimated Savings")
    col_left, col_right = st.columns(2)

    with col_left:
        summary = pd.DataFrame({
            "Metric": [
                "Scenario",
                "Real Cost (€)",
                "Simulated Cost (€)",
                "Estimated Savings (€)"
            ],
            "Value": [
                benchmark_label.upper(),
                f"€ {real_cost:,.0f}".replace(",", " "),
                f"€ {sim_cost:,.0f}".replace(",", " "),
                f"€ {savings:,.0f}".replace(",", " ")
            ]
        })
        st.dataframe(summary, use_container_width=True, hide_index=True)

    with col_right:
        waterfall = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute", "relative", "total"],
            x=["Real Cost", "Savings", "Simulated Cost"],
            y=[real_cost, -savings, sim_cost],
            connector={"line": {"color": "#AAB2BD"}},
            decreasing={"marker": {"color": "#2C3E50"}},
            increasing={"marker": {"color": "#E74C3C"}},
            totals={"marker": {"color": "#2980B9"}}
        ))
        waterfall.update_layout(
            title=f"Estimated Savings Applying {benchmark_label.upper()} Benchmark",
            yaxis_title="€",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )
        st.plotly_chart(waterfall, use_container_width=True)

    # ---------------------------
    # Gráfico com filtros laterais
    # ---------------------------
    st.markdown("Contracts Above / Below Benchmark by Variable")
    left_col, right_col = st.columns([1, 3])

    with left_col:
        st.markdown("Filters")

        # Filtro de localização
        loc_options = df['loc'].dropna().unique().tolist()
        selected_locs = st.multiselect("Select Location(s)", options=loc_options, default=loc_options)

        # Filtro de ano de contrato
        min_year, max_year = int(df['contract_year'].min()), int(df['contract_year'].max())
        selected_years = st.slider(
            "Select Contract Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1
        )

    # Aplica os filtros
    df_filtered = df[df['loc'].isin(selected_locs) & df['contract_year'].between(*selected_years)].copy()
    df_filtered['bench_status'] = np.where(df_filtered['gap'] > 0, "Above", "Below")

    with right_col:
        st.markdown("Contracts Above / Below Benchmark by Variable")

        pretty_variable_names = {
            'act_type': "Type of Act",
            'base_price': "Base Price",
            'execution_dummy': "Execution Rate",
            'environmental': "Environmental Criteria",
            'contract_year': "Contract Year",
            'covid_pandemic': "Pandemic Period ",
            'loc': "Location NUTSII",
            'CPV_agrupado': "CPV Group",
            'bidders': "Number of Bidders"
        }

        selected_var = st.selectbox(
            "Choose a variable:",
            options=list(pretty_variable_names.keys()),
            format_func=lambda x: pretty_variable_names[x]
        )

        if selected_var == "base_price":
            bin_edges = [0, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, float('inf')]
            bin_labels = ["<10K", "10K–50K", "50K–100K", "100K–500K", "500K–1M", "1M–5M", "5M+"]
            df_filtered['price_bin'] = pd.cut(df_filtered['base_price'], bins=bin_edges, labels=bin_labels, include_lowest=True)
            group_col = 'price_bin'
            x_label = "Base Price Range"
        else:
            group_col = selected_var
            x_label = pretty_variable_names[selected_var]

        if selected_var == "execution_dummy":
            df_filtered[selected_var] = df_filtered[selected_var].replace({0: "Not Met", 1: "Met"})

        # Agrupar e contar
        gap_counts = (
            df_filtered.groupby([group_col, 'bench_status'])
            .size()
            .reset_index(name='contracts')
        )

        # Plot
        gap_bar = px.bar(
            gap_counts,
            x=group_col, y='contracts',
            color='bench_status',
            barmode='group',
            color_discrete_map={"Above": "#E74C3C", "Below": "#3498DB"},
            labels={'contracts': 'Number of Contracts', group_col: x_label}
        )
        gap_bar.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="black"))
        st.plotly_chart(gap_bar, use_container_width=True)

def load_and_display_sfa():
  

    # Caminho do CSV gerado pelo modelo SFA
    file_path = "Data/dados_completos.csv"

    try:
        df = pd.read_csv(file_path)

        # Verificações mínimas
        required_cols = {'efficiency', 'contract_year', 'loc'}
        if not required_cols.issubset(set(df.columns)):
            st.error(f"CSV is missing required columns: {required_cols - set(df.columns)}")
            return

        # Mostra o dashboard com os filtros e gráficos
        show_efficiency_dashboard(df)

    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except Exception as e:
        st.error(f"Error loading data: {e}")

@st.cache_data
def load_randomforest_data():
    return pd.read_csv("data/randomforest_results.csv")  # ou outro caminho correto

def show_randomforest_tab():
    st.markdown("## 🌲 Random Forest – Risk of Cost Increase")

    df = load_randomforest_data()

    # Slider para threshold de risco
    threshold = st.slider("Select Risk Threshold", 0.1, 0.9, 0.5, 0.05)

    # Métricas agregadas
    risky_contracts = df[df['predicted_prob'] >= threshold]
    safe_contracts  = df[df['predicted_prob'] < threshold]

    col1, col2 = st.columns(2)
    col1.metric("Contracts at Risk", len(risky_contracts))
    col2.metric("Contracts Considered Safe", len(safe_contracts))

    # Gráfico de densidade de probabilidade
    st.markdown("### 🔎 Distribution of Risk Probabilities")
    fig = px.histogram(df, x="predicted_prob", nbins=30, color_discrete_sequence=["#005082"])
    fig.update_layout(xaxis_title="Predicted Probability of Cost Increase", yaxis_title="Number of Contracts")
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar os contratos de maior risco
    st.markdown("### 🚨 Top 10 Contracts with Highest Risk")
    top_risk = df.sort_values("predicted_prob", ascending=False).head(10)
    st.dataframe(top_risk)

    # Policy Implication
    st.markdown("### 🏛️ Policy Implications")
    st.info(f"""
    Contracts with a predicted probability of cost increase above **{threshold:.2f}** should be monitored closely.
    
    Recommended actions:
    - Perform **ex-ante audits** for contracts at risk;
    - Apply **stricter evaluation criteria** in procurement;
    - Promote **greater competition** (e.g., higher number of bidders);
    - Use this model as a **decision-support tool** in early procurement stages.
    """)



def streamlit_dashboard_rf_analysis():
    # CONFIGURAÇÃO STREAMLIT
    st.set_page_config(layout="wide")
    st.title("📊 Análise de Risco de Aumento de Custo com Random Forest")

    # PARÂMETROS
    threshold = 0.065

    @st.cache_data
    def load_data():
        df = pd.read_csv("data/dados_limpos.csv")
        shap_df = pd.read_csv("data/shap_values.csv")
        feature_imp = pd.read_csv("data/feature_importance_rf.csv")
        return df, shap_df, feature_imp

    df, shap_df, feature_imp = load_data()

    # VERIFICAR CAMPOS
    if "custo_aumentou" not in df.columns or "risk_prob" not in df.columns:
        st.error("Faltam colunas necessárias como 'custo_aumentou' ou 'risk_prob'.")
        return

    # MÉTRICAS GERAIS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 % Contratos com Aumento", f"{(df['custo_aumentou']==1).mean()*100:.2f}%")
    with col2:
        st.metric("🚨 % Classificados como Risco", f"{(df['risk_prob']>=threshold).mean()*100:.2f}%")
    with col3:
        sim_df = df.copy()
        custo_real = sim_df['effective_total_price'].sum()
        preco_seguro = sim_df.loc[sim_df['risk_prob'] < threshold, 'effective_total_price'].mean()
        sim_df['price_sim'] = sim_df['effective_total_price']
        sim_df.loc[sim_df['risk_prob'] >= threshold, 'price_sim'] = preco_seguro
        custo_sim = sim_df['price_sim'].sum()
        poupanca = custo_real - custo_sim
        st.metric("📉 Poupança Simulada", f"€ {poupanca:,.0f}".replace(",", " "))

    # IMPORTÂNCIA DAS FEATURES
    st.markdown("### 🧠 Importância das Features (SHAP)")
    fig1 = px.bar(
        shap_df.sort_values("importance", ascending=False).head(10),
        x="importance",
        y="feature",
        orientation='h',
        color="importance",
        color_continuous_scale="blues",
        labels={"importance": "SHAP Value", "feature": "Feature"},
    )
    st.plotly_chart(fig1, use_container_width=True)

    # DISTRIBUIÇÃO DAS PROBABILIDADES
    st.markdown("### 🔍 Distribuição da Probabilidade de Risco")
    fig2 = px.histogram(
        df,
        x="risk_prob",
        color="custo_aumentou",
        nbins=50,
        barmode="overlay",
        histnorm="percent",
        color_discrete_map={0: "green", 1: "red"},
        labels={"risk_prob": "Probabilidade de Aumento", "custo_aumentou": "Aumento Real"},
    )
    st.plotly_chart(fig2, use_container_width=True)

    # TABELA DOS CONTRATOS MAIS ARRISCADOS
    st.markdown("### 📄 Principais Contratos Classificados com Risco Elevado")
    st.dataframe(
        df[['base_price', 'bidders', 'loc', 'CPV_agrupado', 'contract_year', 'risk_prob', 'custo_aumentou']]
        .sort_values("risk_prob", ascending=False)
        .head(20)
    )

    # FOOTER
    st.info(f"""
    🔍 Este painel mostra os resultados do modelo Random Forest para prever risco de aumento de custo.
    Contratos com `risk_prob >= {threshold}` são considerados de risco e substituídos por um preço médio de referência.
    """)

# Para correr o dashboard: basta chamar esta função no final do script
if __name__ == "__main__":
    streamlit_dashboard_rf_analysis()