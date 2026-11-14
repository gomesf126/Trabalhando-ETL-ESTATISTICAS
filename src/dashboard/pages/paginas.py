import streamlit  as st
from src.analytics.charts import grafico_line_estatisticas_produto_mensal
from src.analytics.charts import criar_grafico_pizza_por_mes
from src.analytics.metricas import gerar_metricas_estatisticas_produto_mensal


def visao_geral(df, ano_selecionado):
    # ========Melhor produto mensal

    subtitulo, select = st.columns([7, 1])

    with subtitulo:
        st.subheader("Melhor produto mensal ")
    with select:
        quantidade = st.selectbox(
            label='Quantidade',
            options=[2, 5, 7, 10],
            index=1,
            label_visibility="collapsed",
            key='selectbox_pagina01'
        )

    # --- 1º Container: Evolução Temporal (Linhas) ---
    grafico1 = st.container(border=True)
    with grafico1:
        st.subheader("Evolução Mensal do Faturamento")
        fig_linha = grafico_line_estatisticas_produto_mensal(
            funcao_metrica=gerar_metricas_estatisticas_produto_mensal,
            df=df,
            ano=ano_selecionado,
            quantidade=quantidade,
        )
        st.plotly_chart(fig_linha, width="stretch")

    # --- 2º Container: Participação por Mês Específico (Pizza) ---

    # --- 2º Container: Participação por Mês Específico (Pizza) ---
    grafico2 = st.container(border=True)
    with grafico2:
        # Cabeçalho interno do container: Título à esquerda e Seletor de Mês à direita (estilo compacto)
        sub_pizza, sel_mes = st.columns([7, 1])

        with sub_pizza:
            st.subheader("Participação Percentual por Mês")

        # Extrai a lista de meses disponíveis com base na quantidade selecionada
        dados_base = gerar_metricas_estatisticas_produto_mensal(
            df=df, ano=ano_selecionado, quantidade=quantidade
        )
        meses_disponiveis = dados_base["MES"].unique()

        with sel_mes:
            mes_escolhido = st.selectbox(
                label="Mês",
                options=meses_disponiveis,
                label_visibility="collapsed",
                key="selectbox_mes_pizza",
            )

        # Gera o gráfico de pizza filtrado por esse mês e quantidade
        fig_pizza = criar_grafico_pizza_por_mes(
            funcao_metrica=gerar_metricas_estatisticas_produto_mensal,
            df=df,
            ano=ano_selecionado,
            mes_selecionado=mes_escolhido,
            quantidade=quantidade,
        )
        st.plotly_chart(fig_pizza, width="stretch")

    return grafico1, grafico2