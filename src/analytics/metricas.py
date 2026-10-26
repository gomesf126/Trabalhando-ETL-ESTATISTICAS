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


def gerar_metricas_com_moda(df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
    """Calcula a moda do produto e do faturamento para vendas válidas (> 0)."""
    # 1. Filtro de ano
    filtro = gerar_query(df, ano)

    # 2. Filtro de faturamento positivo no DataFrame JA FILTRADO por ano
    dados_validos = filtro.loc[ filtro["FATURAMENTO_LIQUIDO"] > 0, ["ID-PRODUTO", "PRODUTO", "MES", "MES_NUM", "FATURAMENTO_LIQUIDO"]]

    if dados_validos.empty:
        return pd.DataFrame(
            [{
                "PRODUTO_MODA": None,
                "FATURAMENTO_MODA": None,
                "QUANTIDADE_MODA": 0,
            }]
        )

    # 3. Uso da funcao calcular_moda do modulo statistics.py
    produto_moda_val = calcular_moda(dados_validos["PRODUTO"])
    fat_moda_val = calcular_moda(dados_validos["FATURAMENTO_LIQUIDO"])

    # 4. Contagem direta das ocorrencias do produto moda
    quantidade = (dados_validos["PRODUTO"] == produto_moda_val).sum()

    resultado = {
        "PRODUTO_MODA": produto_moda_val,
        "FATURAMENTO_MODA": fat_moda_val,
        "QUANTIDADE_MODA": quantidade,
    }

    return pd.DataFrame([resultado])


def gerar_metricas_estatisticas_produto( df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
    """Calcula métricas estatísticas agregadas por ID e Nome do produto."""
    filtro = gerar_query(df, ano)
    filtrado = filtro.loc[filtro["FATURAMENTO_LIQUIDO"] > 0, ["ID-PRODUTO", "PRODUTO", "MES", "MES_NUM", "FATURAMENTO_LIQUIDO"]]

    resultado = (filtrado.groupby( ["PRODUTO", "MES", "MES_NUM"], as_index=False)
        .agg(
            VARIACAO_FATURAMENTO=("FATURAMENTO_LIQUIDO", calcular_variancia),
            MEDIA_PRODUTO=("FATURAMENTO_LIQUIDO", calcular_media),
            MEDIANA_PRODUTO=("FATURAMENTO_LIQUIDO", calcular_mediana),
            DESVIO_PADRAO_PRODUTO=("FATURAMENTO_LIQUIDO", calcular_desvio_padrao)
        )
         # Ordena primeiro por Produto (A-Z) e depois por Mês (Janeiro a Dezembro)
         .sort_values(by=["PRODUTO", "MES_NUM"], ascending=[True, True])
         )

    return resultado


def gerar_metricas_estatisticas_geral(df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
    """Calcula métricas estatísticas gerais de faturamento."""
    filtro = gerar_query(df, ano)
    vendas = filtro.loc[filtro["FATURAMENTO_LIQUIDO"] > 0, "FATURAMENTO_LIQUIDO"]

    # Uso das funcoes de estatistica customizadas
    resultado = pd.DataFrame([{
        "MEDIA_GERAL": calcular_media(vendas),
        "MEDIANA_GERAL": calcular_mediana(vendas),
        "VARIACAO_GERAL": calcular_variancia(vendas),
        "DESVIO_PADRAO_GERAL": calcular_desvio_padrao(vendas)
    }])

    return resultado


def gerar_quartis_produto_ano(df: pd.DataFrame, ano: int = None) -> pd.DataFrame:
  """Calcula os quartis de faturamento por produto considerando o ano inteiro."""
  filtro = gerar_query(df, ano)

  # Pega todas as vendas válidas do ano, sem separar por mês
  filtrado = filtro.loc[
      filtro["FATURAMENTO_LIQUIDO"] > 0, ["ID-PRODUTO", "PRODUTO", "FATURAMENTO_LIQUIDO"]
  ]

  # Agrupa apenas por Produto e calcula os quartis anuais
  resultado = (
      filtrado.groupby(["ID-PRODUTO", "PRODUTO"], as_index=False)
      .agg( QUARTIS_ANUAL=("FATURAMENTO_LIQUIDO", calcular_quartis ))
      .sort_values(by="PRODUTO", ascending=True)
  )

  return resultado






