import streamlit as st
from src.analytics.metricas import gerar_metricas_estatisticas_anual


def gerar_cards(df, ano_selecionado):
    #pegar os dados da função para os cards
    estatistica= gerar_metricas_estatisticas_anual(df, ano_selecionado)
    card = st.columns(5)

    with card[0]:
        with st.container(border=True):
            st.metric(
                label="💰 Faturamento anual",
                value=estatistica['FATURAMENTO_TOTAL']
            )
    with card[1]:
        with st.container(border=True):
            st.metric(
                label="📈 Média anual",
                value=estatistica['MEDIA_GERAL']
            )
    with card[2]:
        with st.container(border=True):
            st.metric(
                label="🎯 Mediana anual",
                value=estatistica['MEDIANA_GERAL']
            )
    with card[3]:
        with st.container(border=True):
            st.metric(
                label="📊 Variação anual",
                value=estatistica['VARIACAO_GERAL']
            )
    with card[4]:
        with st.container(border=True):
            st.metric(
                label="📉 Desvio Padrão anual",
                value=estatistica['DESVIO_PADRAO_GERAL']
            )
