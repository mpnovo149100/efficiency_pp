import streamlit as st
import plotly.express as px
import pandas as pd

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

binary_mappings = {
    'execution_dummy': {0: "Execution Not Met", 1: "Execution Met"},
    'environmental': {0: "No Environmental Criteria", 1: "Environmental Criteria Applied"},
    'covid_pandemic': {0: "Non-pandemic Period", 1: "Pandemic Period"}
}

def format_group_val(val, col):
    if col in binary_mappings:
        return binary_mappings[col].get(val, str(val))
    if isinstance(val, (int, float)):
        if val == int(val):
            return str(int(val))
        else:
            return f"{val:.2f}"
    return str(val)

def show_efficiency_dashboard(df):


    # Filtros
    left_col, right_col = st.columns([1, 3])
    with left_col:
        st.markdown("#### Filters")
        loc_options = df['loc'].dropna().unique().tolist()
        selected_locs = st.multiselect("Select Location(s)", options=loc_options, default=loc_options)
        min_year, max_year = int(df['contract_year'].min()), int(df['contract_year'].max())
        selected_years = st.slider("Select Contract Year Range", min_value=min_year, max_value=max_year,
                                   value=(min_year, max_year), step=1)

    df_filtered = df[df['loc'].isin(selected_locs) & df['contract_year'].between(*selected_years)]

    with right_col:
        st.markdown("#### Efficiency Distribution")
        fig_dist = px.histogram(
            df_filtered,
            x='efficiency',
            nbins=20,
            title="Distribution of Efficiency Scores",
            labels={'efficiency': 'Efficiency Score'},
            color_discrete_sequence=['#0B2C54']
        )
       
        fig_dist.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='black'))
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("#### Average Efficiency by Group")

    # Variáveis permitidas no dropdown
    dropdown_vars = list(pretty_variable_names.keys())
    group_col = st.selectbox("Group By Variable", dropdown_vars, format_func=lambda x: pretty_variable_names.get(x, x))

    # Eficiência média por grupo
    mean_eff = (
        df_filtered.groupby(group_col)['efficiency']
        .mean()
        .reset_index()
        .sort_values(by='efficiency', ascending=False)
    )

    # Discretizar base_price se selecionado
    if group_col == "base_price":
        bins = [0, 10000, 50000, 100000, 500000, 1_000_000, 5_000_000, 10_000_000, df['base_price'].max()]
        labels = ['<10K', '10K–50K', '50K–100K', '100K–500K', '500K–1M', '1M–5M', '5M–10M', '>10M']
        df_filtered['base_price_bin'] = pd.cut(df_filtered['base_price'], bins=bins, labels=labels)
        group_col = 'base_price_bin'
        mean_eff = (
            df_filtered.groupby(group_col)['efficiency']
            .mean()
            .reset_index()
            .sort_values(by='efficiency', ascending=False)
        )

    # Gráfico
    fig_bar = px.bar(
        mean_eff,
        x=group_col,
        y='efficiency',
        title=f"Average Efficiency by {pretty_variable_names.get(group_col, group_col)}",
        color='efficiency',
        color_continuous_scale=[
        "#cce4f6",  # azul claro mais visível
        "#1f77b4",  # azul médio
        "#0B2C54"   # azul escuro (corporativo)
    ],
        labels={'efficiency': 'Average Efficiency'}
    )
    fig_bar.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(color='black'))
    st.plotly_chart(fig_bar, use_container_width=True)

    # Alerta de baixa eficiência com comparação
    if not mean_eff.empty:
        min_row = mean_eff.iloc[-1]
        max_row = mean_eff.iloc[0]

        min_val = format_group_val(min_row[group_col], group_col)
        max_val = format_group_val(max_row[group_col], group_col)

        st.markdown(f"""
         ** Efficiency Alert**  
        The lowest average efficiency was observed in **{min_val}**, with a score of **{min_row['efficiency']:.2f}**.  
        In contrast, the highest was **{max_row['efficiency']:.2f}** in **{max_val}**.
        """)