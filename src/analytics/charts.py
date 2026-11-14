
import plotly.express as px
import streamlit as st

def grafico_bar(funcao_metrica, df, ano, x,y, color,orientacao):

    base = funcao_metrica(df ,  ano)
    if orientacao.lower() == "v":
        fig = px.bar(
            base,
            x=y, # Categoria vai para o X no gráfico vertical
            y=x, # Valor numérico vai para o Y
            color=color,
            orientation='v',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        hovertemplate_str = "<b>%{x}</b><br>%{y:,.2f}<br><extra></extra>"

    else:
        fig = px.bar(
            base,
            x=y, # Categoria vai para o X no gráfico vertical
            y=x, # Valor numérico vai para o Y
            color=color,
            orientation='h',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        hovertemplate_str = "<b>%{y}</b><br>%{x:,.2f}<br><extra></extra>"
    fig.update_traces(
        hovertemplate=  hovertemplate_str,
        textposition='outside'
    )
    fig.update_layout(
        #title=title if title else "Gráfico analítico",
        #title_x=0.5,
        xaxis_title= None,
        yaxis_title= None,
        template='plotly_white',
        showlegend=True,
        #bargap=0.15,  # Diminui o espaço entre as barras, deixando-as mais grossas
        #height=400 # Opcional: define uma altura fixa ideal para o container do Streamlit
    )

    return fig


def criar_grafico_pizza_por_mes(funcao_metrica, df, ano,mes_selecionado, quantidade):
    # Pega nos dados métricos gerais
    base = funcao_metrica(df, ano, quantidade)

    # Filtra estritamente para o mês escolhido pelo utilizador
    base_mes = base[base["MES"] == mes_selecionado]

    # Agrupa para o gráfico de pizza daquele mês
    df_pizza = (
        base_mes.groupby("PRODUTO", as_index=False)["FATURAMENTO_TOTAL_MENSAL"]
        .sum()
        .sort_values(by="FATURAMENTO_TOTAL_MENSAL", ascending=False)
    )

    fig = px.pie(
        df_pizza,
        names="PRODUTO",
        values="FATURAMENTO_TOTAL_MENSAL",
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )
    return fig

def grafico_line_estatisticas_produto_mensal(funcao_metrica, df, ano, quantidade):
    base = funcao_metrica(df, ano, quantidade)
    fig = px.line(
        base,
        x='MES_NUM',
        y='FATURAMENTO_TOTAL_MENSAL',
        color= 'PRODUTO',# Separa uma linha para cada produto com cores diferentes
        markers=True,# Adiciona bolinhas nos pontos de cada mês
        hover_name='PRODUTO',# Mostra o nome do produto em destaque ao passar o mouse
        labels={
            "MES_NUM":'Mês',
            "FATURAMENTO_TOTAL_MENSAL":'Faturamento líquido R$',
            "PRODUTO":"Produto"
        }
    )
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=base['MES_NUM'].unique(),
            ticktext=base['MES'].unique()
        )
    )
    return fig


#statistica_mensal = gerar_metricas_estatisticas_produto_mensal(df=df, ano=ano_selecionado)

# Pega o mês e o número do mês, remove duplicadas e ordena pela ordem cronológica
#opcao_mes = (
#    statistica_mensal[['MES', 'MES_NUM']]
#    .drop_duplicates()
#    .sort_values('MES_NUM')
#    ['MES'] # Extrai apenas a lista de nomes dos meses ordenada
#)