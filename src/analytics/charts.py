import pandas as pd
from numpy.ma.core import empty

from src.analytics.statistics import (
    calcular_desvio_padrao,
    calcular_media,
    calcular_mediana,
    calcular_moda,
    calcular_variancia,
    calcular_quartis
)

def gerar_query(df:pd.DataFrame, ano: int=None):
    if ano is not None:
        return df.query("ANO == @ano")
    return df

def gerar_metricas_com_moda_global(df:pd.DataFrame, ano:int=None):
    df_filtro = gerar_query(df, ano)
    #filtrar sómente faturamento > 0
    df_filtro = df_filtro.loc[df_filtro['FATURAMENTO_LIQUIDO'] > 0, ['ID-PRODUTO','PRODUTO','FATURAMENTO_LIQUIDO','ANO','MES_NUM','MES']]
    #gerar a moda por produto e faturamento
    moda_produto =calcular_moda(df_filtro['ID-PRODUTO'])
    moda_faturamento = calcular_moda(df_filtro['FATURAMENTO_LIQUIDO'])

    #moda do produto campeão
    moda ={
        'MODA_PRODUTO': moda_produto,
        'MODA_FATURAMENTO':moda_faturamento
    }

    return moda

def gerar_metricas_com_moda_individual(df: pd.DataFrame, ano: int = None):
        df_filtro = gerar_query(df, ano)
        # filtrar sómente faturamento > 0
        df_filtro = df_filtro.loc[ df_filtro['FATURAMENTO_LIQUIDO'] > 0, ['ID-PRODUTO', 'PRODUTO', 'FATURAMENTO_LIQUIDO', 'ANO', 'MES_NUM','MES']]


        #pegar os top 10 produtos do ano
        moda = (df_filtro
        .groupby('PRODUTO', as_index=False)
        .agg(
            MODA_PRODUTO=("ID-PRODUTO", calcular_moda),
            MODA_FATURAMENTO=("FATURAMENTO_LIQUIDO", calcular_moda)
        )
        .sort_values(['MODA_FATURAMENTO','MODA_PRODUTO'], ascending=[False, True])
        .head(10) )

        return moda

