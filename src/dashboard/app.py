import streamlit as st
import pandas as pd

from src.extract.extrair import extrair_arquivo
from src.pipeline.pipeline import pipeline
from src.dashboard.pages.cards import gerar_cards
from src.dashboard.pages.paginas import visao_geral
#=================================================
            #CONFIGURAÇÃO DA PAGINA
#=================================================
st.set_page_config(page_title="Dashboard 2027", layout="wide")

#=================================================
#ACESSANDO O DATAFRAME
#=================================================
with st.spinner("Extraindo e processando dados..."):
    df_raw = extrair_arquivo()
    df = pipeline(df_raw)
#=================================================
#CONVERVER MES E ANO EM NUMERO INTEIRO
df['ANO'] = pd.to_numeric(df['ANO']).astype('Int64')
df['MES_NUM']= pd.to_numeric(df['MES_NUM']).astype("Int64")

ano =sorted(df['ANO'].dropna().unique(),  reverse=True)

#CAIXA DE SELEÇÃO LATERAL
ano_selecionado = st.sidebar.selectbox(
    label="ANO",
    options=ano
)


st.title(f"DASHBOARD de {ano_selecionado}")
st.write("Seja bem vindo Fabiano")
st.divider()

           #CARDS + METRICAS
#=================================================

gerar_cards(df ,ano_selecionado)

#======CARDS
st.divider()

#=================================================
        #MENU
#=================================================
if "visão_geral" not in st.session_state:
    st.session_state.pagina_atual = 'visão_geral'

menu= st.columns([0.5, 0.5, 0.5])

with menu[0]:
    if st.button("Visão Geral", use_container_width=True):
        st.session_state.pagina_atual = 'visão_geral'
with menu[1]:
    if st.button("Análise de Produtos", use_container_width=True):
        st.session_state.pagina_atual="analise_produto"
with menu[2]:
    if st.button("Estatísticas & Distribuição", use_container_width=True):
        st.session_state.pagina_atual="estatistica_distribuicao"
st.divider()

#=================================================
        #PAGINA Visão Geral
#=================================================
if st.session_state.pagina_atual == 'visão_geral':
    visao_geral(df, ano_selecionado)

#=================================================
        #MENU Análise de Produtos
#=================================================
if st.session_state.pagina_atual == 'analise_produto':
    st.title("Análise de Produtos")

#=================================================
        #MENU Estatísticas & Distribuição
#=================================================
if st.session_state.pagina_atual == "estatistica_distribuicao":
    st.title("Estatísticas & Distribuição")


