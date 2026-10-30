import pandas as pd
from src.analytics.statistics import (
    calcular_desvio_padrao,
    calcular_media,
    calcular_mediana,
    calcular_moda,
    calcular_variancia,
    calcular_quartis
)


def gerar_query(df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
    """Filtra o DataFrame pelo ano informado.
    Se ano for None, retorna o DataFrame original.
    """
    if ano is not None:
        return df.query("ANO == @ano")
    return df


def gerar_metricas_com_moda_global(df:pd.DataFrame, ano:int=None):
    df_filtro = gerar_query(df, ano)
    #filtrar sómente faturamento > 0
    df_filtro = df_filtro.loc[df_filtro['FATURAMENTO_LIQUIDO'] > 0, ['ID-PRODUTO','PRODUTO','FATURAMENTO_LIQUIDO','ANO','MES_NUM','MES']]
    #segurança caso venha o dataframe vazio
    if df_filtro.empty:
        return pd.DataFrame([{
            'MODA_PRODUTO': None,
            'MODA_PRODUTO_ID': None,
            'MODA_FATURAMENTO': None
        }])

    #gerar a moda por produto e faturamento
    moda_produto_id =calcular_moda(df_filtro['ID-PRODUTO'])
    moda_faturamento = calcular_moda(df_filtro['FATURAMENTO_LIQUIDO'])


    #descobrir o nome do produto
    moda_produto = df_filtro.loc[df_filtro['ID-PRODUTO'] == moda_produto_id, 'PRODUTO'].iloc[0]
    #moda do produto campeão
    moda ={
        'MODA_PRODUTO': moda_produto,
        'MODA_PRODUTO_ID': moda_produto_id,
        'MODA_FATURAMENTO':moda_faturamento
    }

    return pd.DataFrame([moda])

def gerar_metricas_com_moda_individual(df: pd.DataFrame, ano: int = None):
        df_filtro = gerar_query(df, ano)
        # filtrar sómente faturamento > 0
        df_filtro = df_filtro.loc[ df_filtro['FATURAMENTO_LIQUIDO'] > 0, ['ID-PRODUTO', 'PRODUTO', 'FATURAMENTO_LIQUIDO', 'ANO', 'MES_NUM','MES']]


        #pegar os top 10 produtos do ano
        moda = (df_filtro
        .groupby('PRODUTO', as_index=False)
        .agg(
            MODA_PRODUTO=("ID-PRODUTO", calcular_moda),
            MODA_FATURAMENTO=("FATURAMENTO_LIQUIDO", calcular_moda),
            QUANTIDADE      =('ID-PRODUTO', 'count')
        )
        .sort_values(['MODA_FATURAMENTO','MODA_PRODUTO'], ascending=[False, True])
        .head(10) )

        return moda



def gerar_metricas_estatisticas_produto_mensal( df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
    """Calcula métricas estatísticas agregadas por ID e Nome do produto."""
    filtro = gerar_query(df, ano)
    filtrado = filtro.loc[filtro["FATURAMENTO_LIQUIDO"] > 0, ["ID-PRODUTO", "PRODUTO", "MES", "MES_NUM", "FATURAMENTO_LIQUIDO"]]

    resultado = (filtrado.groupby( ["PRODUTO", "MES", "MES_NUM"], as_index=False)
        .agg(
            FATURAMENTO_TOTAL_MENSAL=("FATURAMENTO_LIQUIDO", "sum"),
            VARIACAO_FATURAMENTO=("FATURAMENTO_LIQUIDO", calcular_variancia),
            MEDIA_PRODUTO=("FATURAMENTO_LIQUIDO", calcular_media),
            MEDIANA_PRODUTO=("FATURAMENTO_LIQUIDO", calcular_mediana),
            DESVIO_PADRAO_PRODUTO=("FATURAMENTO_LIQUIDO", calcular_desvio_padrao)
        )
         # Ordena primeiro por Produto (A-Z) e depois por Mês (Janeiro a Dezembro)
         .sort_values(by=["PRODUTO", "MES_NUM"], ascending=[True, True])
         )

    return resultado


def gerar_metricas_estatisticas_anual(df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
    """Calcula métricas estatísticas gerais de faturamento."""
    filtro = gerar_query(df, ano)
    vendas = filtro.loc[filtro["FATURAMENTO_LIQUIDO"] > 0, "FATURAMENTO_LIQUIDO"]

    if  vendas.empty:
            return pd.DataFrame([{
            "FATURAMENTO_TOTAL": None,
            "MEDIA_GERAL":  None,
            "MEDIANA_GERAL":  None,
            "VARIACAO_GERAL":  None,
            "DESVIO_PADRAO_GERAL": None
        }])
    # Uso das funcoes de estatistica customizadas
    return pd.DataFrame([{
        "FATURAMENTO_TOTAL": vendas.sum(),
        "MEDIA_GERAL": calcular_media(vendas),
        "MEDIANA_GERAL": calcular_mediana(vendas),
        "VARIACAO_GERAL": calcular_variancia(vendas),
        "DESVIO_PADRAO_GERAL": calcular_desvio_padrao(vendas)
    }])




def gerar_quartis_geral_ano(df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
  """Calcula os quartis de faturamento por produto considerando o ano inteiro."""
  filtro = gerar_query(df, ano)

  vendas = filtro.loc[filtro["FATURAMENTO_LIQUIDO"] > 0,  "FATURAMENTO_LIQUIDO"]
  #SEGURANÇA CASO VENHA O DATAFRAME VAZIO
  if vendas.empty:
      return pd.DataFrame([{
           "Q1":None,
           "MEDIANA":None,
           "Q3":None
          }])

  Q1, MEDIANA, Q3 = calcular_quartis(vendas)

  return pd.DataFrame([{
      "Q1": Q1,
      "MEDIANA": MEDIANA,
      "Q3": Q3
  }])




