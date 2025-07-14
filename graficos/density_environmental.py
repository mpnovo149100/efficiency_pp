import pandas as pd
import plotly.express as px
import plotly.io as pio

def plot_density_ln_effective_price_by_environmental(df: pd.DataFrame, output_pdf_path='grafico_criterio_ambiental.pdf'):
    df = df.copy()

    # Remover linhas com NaN nas colunas necessárias
    df = df.dropna(subset=['ln_effective_total_price', 'environmental'])

    # Mapear valores binários para texto
    df['Environmental Criteria'] = df['environmental'].map({
        0: 'No Criteria',
        1: 'Criteria'
    })

    # Criar o gráfico de densidade
    fig = px.histogram(
        df,
        x='ln_effective_total_price',
        color='Environmental Criteria',
        histnorm='density',
        barmode='overlay',
        opacity=0.5,
        color_discrete_map={
            'No Criteria': '#bcbcbc',
            'Criteria': '#1f3c88'
        },
        labels={
            'ln_effective_total_price': 'Logₑ(Effective Price)',
            'Environmental Criteria': 'Environmental'
        }
    )

    fig.update_layout(
        xaxis_title='Logₑ(Effective Price)',
        yaxis_title='Density',
        legend_title='Environmental Criteria',
        template='simple_white',
        margin=dict(l=40, r=30, t=60, b=40)
    )

    # Guardar como PDF
    pio.write_image(fig, output_pdf_path, format='pdf')

# ----------- Execução do script -----------
# Lê os dados do CSV
df = pd.read_csv("Data/dados_completos.csv")

# Gera e guarda o gráfico como PDF
plot_density_ln_effective_price_by_environmental(df, "Graficos_tese/grafico_criterio_ambiental.pdf")