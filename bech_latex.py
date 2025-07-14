import pandas as pd

def compute_efficiency_gap_by_variable(df: pd.DataFrame,
                                       variables: list,
                                       efficiency_col: str = "efficiency",
                                       percentiles: list = [0.50, 0.75, 0.90]) -> pd.DataFrame:
    results = []

    for var in variables:
        if var not in df.columns:
            continue

        for q in percentiles:
            benchmark = df[efficiency_col].quantile(q)

            # Cálculo correto: média da eficiência por categoria - benchmark
            gap_by_category = df.groupby(var)[efficiency_col].mean() - benchmark

            # Média dos gaps entre as categorias da variável
            avg_gap = gap_by_category.mean()

            results.append({
                "Variable": var,
                f"Gap at P{int(q*100)}": round(avg_gap, 3)
            })

    # Constrói tabela
    result_df = pd.DataFrame(results)

    # Pivot para ter colunas por percentil
    result_df = result_df.pivot_table(index="Variable", aggfunc="first")

    # Ordena colunas por percentil
    ordered_cols = [f"Gap at P{int(q*100)}" for q in percentiles if f"Gap at P{int(q*100)}" in result_df.columns]
    result_df = result_df[ordered_cols].reset_index()

    return result_df

# Carrega os dados
df = pd.read_csv("Data/dados_completos.csv")

variables_to_check = [
    "bidders",
    "covid_pandemic",
    "execution_dummy",  # podes remover se necessário
    "act_type",
    "CPV_agrupado",
    "loc",
    "contract_year",
    "ln_base_price",
    "environmental"
]

# Calcula a tabela
gap_table = compute_efficiency_gap_by_variable(df, variables_to_check)

# Exporta
gap_table.to_csv("gap_summary_table.csv", index=False)
print(gap_table.to_latex(index=False, float_format="%.3f"))