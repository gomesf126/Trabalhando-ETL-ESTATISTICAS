import streamlit as st
import pandas as pd

# 1. Configuração da página DEVE ser a primeira coisa do Streamlit
st.set_page_config(page_title="Dashboard 2027", layout="wide")

from src.extract.extrair import extrair_arquivo
from src.pipeline.pipeline import pipeline

from src.analytics.metricas import (
    gerar_quartis_geral_ano,
    gerar_metricas_estatisticas_anual,
    gerar_metricas_estatisticas_produto_mensal,
    gerar_metricas_com_moda_global,
    gerar_metricas_com_moda_individual
)

from src.analytics.charts import grafico_bar

st.title("DASHBOARD 2027")
st.write("Seja bem vindo Fabiano")

# 2. Carregamento dos dados com feedback visual
with st.spinner("Extraindo e processando dados..."):
    df_row = extrair_arquivo()
    df = pipeline(df_row)




# E depois a chamada normal:
fig = grafico_bar(
    funcao_metrica=gerar_metricas_com_moda_individual,
    df=df,
    ano=None,
    x='MODA_FATURAMENTO',
    y='PRODUTO',
    color="MODA_PRODUTO",
    orientacao="v"
)

st.plotly_chart(fig, width='stretch')

