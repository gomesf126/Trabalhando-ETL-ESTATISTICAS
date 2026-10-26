import pandas as pd
from src.transform.limpeza import (
padronizar_colunas,
padronizar_texto,
padronizar_preco_quantidade,
padronizar_datas,
sinalizar_negativos,
tratar_nulos,
tratar_duplicatas

)
from src.transform.feature_tempo import feature_tempo
from src.transform.feature_churn_produto import feature_churn_produto
from src.transform.feature_churn_cliente import feature_churn_cliente
from src.transform.feature_cliente import feature_cliente
from src.transform.feature_classe_abc import feature_classe_abc
from src.transform.feature_produto import feature_produto
from src.transform.feature_tempo import feature_tempo

CLEANING = [
    padronizar_colunas,
    padronizar_texto,
    padronizar_preco_quantidade,
    padronizar_datas,
    tratar_nulos,
    sinalizar_negativos,
    tratar_duplicatas
]
ENGINEERING =[
    feature_tempo,
    feature_produto,
    feature_cliente,

    feature_churn_produto,
    feature_churn_cliente,
    feature_classe_abc
]

def criar_pipeline(df:pd.DataFrame, etapas: list)->pd.DataFrame:
    for funcao in etapas:
        #print(f"Executando : {funcao.__name__}")
        df=funcao(df)
    return df