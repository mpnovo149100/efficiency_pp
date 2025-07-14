import streamlit as st
import base64
from tab_content import new_dashboard_tab, load_and_display_sfa
from simulate_costs import show_rf_cost_mitigation_dashboard
from whatif import what_if_dashboard
st.set_page_config(layout="wide") 
from policy_impl_recom import display_policy_recommendations
from bencharming import show_benchmark_metrics
# Codifica a imagem do logótipo
with open("Data/logo.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

# ---------- Cabeçalho e estilo ----------
st.markdown(f"""  
    <style>  
        .header {{  
            background-color: white;  
            padding: 15px 40px;  
            position: fixed;  
            top: 0;  
            left: 0;  
            right: 0;  
            display: flex;  
            align-items: center;  
            z-index: 999;  
            border-bottom: 1px solid #ccc;
        }}  

        .header img {{  
            height: 60px;  
            margin-right: 20px;  
        }}  

        .header h1 {{  
            color: #000000;  
            font-size: 26px;  
            margin: 0;  
        }}  

        .stApp {{  
            margin-top: 90px;  
            margin-bottom: 60px;  
        }}  

        .footer {{  
            background-color: #404041;  
            color: white;  
            padding: 10px;  
            position: fixed;  
            bottom: 0;  
            left: 0;  
            right: 0;  
            text-align: center;  
            font-size: 14px;  
            z-index: 999;  
        }}  

        .metric-container {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            gap: 20px;
        }}

        .metric-card {{
            flex: 1;
            background-color: white;
            border: 3px solid #86BC25;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}

        .metric-title {{
            font-size: 16px;
            color: #333;
            margin-bottom: 5px;
        }}

        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            color: #000;
        }}
    </style>  

    <div class="header">  
        <img src="data:image/png;base64,{encoded_logo}">  
        <h1>Efficiency in Public Procurement of Healthcare Services in Portugal</h1>  
    </div>  

    <div class="footer">  
        © 2025 NOVA IMS — Design and Developed by Mariana Novo  
    </div>  
""", unsafe_allow_html=True)

# ---------- Tabs principais ----------
tab1, tab2, tab3, tab4 = st.tabs(["Welcome", "Dashboard", "Policy Simulator", "Policy Recommendations"])

with tab1:
    st.markdown("#### User Guide for the Platform")

    st.write("""
    ##### Purpose of the Tool
    This interactive application was developed to support the assessment of efficiency in public procurement within the Portuguese healthcare sector.
    It enables the exploration of contract patterns, risk factors, and the simulation of potential savings using real data.

    ##### Main Modules

    - **Dashboard**  
      This module allows users to explore interactive visualisations of several key variables.  
      You can select a variable from the dropdown menu to view relevant plots and contextual insights automatically.

    - **Policy Simulator**  
      This module simulates potential cost savings and supports policy scenario analysis using three approaches:
        - **Benchmarking (Percentiles):**  
          Estimates how much could be saved if contracts matched the efficiency of the 50th, 75th, or 90th percentiles.
        - **Risk Mitigation via Machine Learning:**  
          Uses a Random Forest model to identify high-risk contracts and estimates savings if better management had been applied.
        - **What-if Scenario Analysis:**  
          Enables users to simulate alternative values (e.g., number of bidders, execution timing) and visualize their estimated impact on procurement costs.
        - **Stochastic Frontier Analysis (SFA):**  
          Presents technical efficiency scores and model results for each contract, supporting evidence-based benchmarking.

    - **Policy Recommendations**
        This section provides actionable insights based on the analysis, helping stakeholders make informed decisions to improve procurement efficiency.

    ###### Target Users
    This tool is designed for policy makers, public managers, and analysts, offering a structured interface for interpreting complex procurement data through visual storytelling.
    """)
with tab2:
    new_dashboard_tab()

with tab3:


    # Botões lado a lado
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("SFA", key="sfa"):
            st.session_state.active_tab = 'sfa'

    with col2:
        if st.button("Benchmarking", key="bench"):
            st.session_state.active_tab = 'bench'
         

    with col3:
        if st.button("Random Forest", key="rf"):
            st.session_state.active_tab = 'rf'

    with col4:
        if st.button("What-If", key="whatif"):
            st.session_state.active_tab = 'whatif'

    st.markdown("---")  # Separador visual

    # Conteúdo dinâmico depois da seleção
    if st.session_state.get('active_tab') == 'bench':

        show_benchmark_metrics()
    if st.session_state.get('active_tab') == 'sfa':
        load_and_display_sfa()
    if st.session_state.get('active_tab') == 'rf':
        show_rf_cost_mitigation_dashboard()
    if st.session_state.get('active_tab') == 'whatif':
        what_if_dashboard()
  
   
with tab4:
    display_policy_recommendations()