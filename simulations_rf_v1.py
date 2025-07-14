import streamlit as st
import pandas as pd
import plotly.express as px

def show_random_forest_dashboard(file_path="Data/randomforest_results.csv", threshold_rf=0.065):
    st.markdown("## 🌲 Random Forest - Risk Mitigation Scenario")

    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # remover espaços

        # Garantir nomes esperados
        df.rename(columns={"cost_increase": "custo_aumentou"}, inplace=True)

        expected_cols = {"custo_aumentou", "risk_prob", "price_sim_rf"}
        if not expected_cols.issubset(df.columns):
            raise ValueError("Ficheiro deve conter as colunas: custo_aumentou, risk_prob, price_sim_rf")

        # Separar contratos por risco
        df['risco'] = df['risk_prob'].apply(lambda x: 'Alto Risco' if x >= threshold_rf else 'Baixo Risco')

        col1, col2 = st.columns(2)

        with col1:
            st.metric("💰 Custo Total Real", f"€ {df['price_sim_rf'].sum():,.0f}")
            st.metric("📈 Contratos com Aumento de Custo", df['custo_aumentou'].sum())

        with col2:
            custo_real = df[df['custo_aumentou'] == 1]['price_sim_rf'].sum()
            custo_simulado = df['price_sim_rf'].sum()
            poupanca = custo_real - custo_simulado
            st.metric("🔧 Poupança Simulada", f"€ {poupanca:,.0f}")

        # Distribuição de risco
        st.markdown("### 🔍 Distribuição de Probabilidade de Risco")
        fig_hist = px.histogram(df, x='risk_prob', nbins=30,
                                color='risco',
                                color_discrete_map={"Baixo Risco": "#1abc9c", "Alto Risco": "#e74c3c"},
                                labels={'risk_prob': 'Probabilidade de Aumento de Custo'})
        fig_hist.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_hist, use_container_width=True)

        # Boxplot dos custos simulados
        st.markdown("### 💼 Comparação de Custos por Grupo de Risco")
        fig_box = px.box(df, x='risco', y='price_sim_rf', color='risco',
                         color_discrete_map={"Baixo Risco": "#1abc9c", "Alto Risco": "#e74c3c"},
                         labels={'price_sim_rf': 'Custo Simulado'})
        fig_box.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig_box, use_container_width=True)

        # Tabela final
        st.markdown("### 📋 Tabela com Resultados")
        st.dataframe(df[['risk_prob', 'custo_aumentou', 'price_sim_rf']].sort_values(by='risk_prob', ascending=False))

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar ou processar o ficheiro: {e}")