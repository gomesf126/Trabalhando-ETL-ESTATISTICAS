import pandas as pd

def calcular_media(serie:pd.Series )->float:
    if serie is not None and not serie.empty:
        media = serie.mean()
        if pd.notna(media):
            return float(media)
    return float(0.0)

def calcular_mediana(serie:pd.Series)->float:
    #verificar se não está sem dados ou vazio
    if serie is not None and not serie.empty:
        mediana = serie.median()
        #reforçar que só aceite a serie com dados
        if pd.notna(mediana):
            return float(mediana)
    return 0.0

def calcular_moda(serie:pd.Series):
    #verifica, não tem dados
    #verifica, não tem linhas, estrutura sem nada ex Series=([])
    if serie is not None and not serie.empty:
        moda= serie.mode()
        #verifica novamente separando os valores vazios da moda
    #([None, None, None]):
    #O produtos.mode() devolveria uma série sem nenhum item (Series([])).
    #O if not moda.empty: barraria o código antes de tentar fazer .iloc[0], evitando o erro index
        if not moda.empty:
            return moda.iloc[0]
    return None

def calcular_desvio_padrao(serie: pd.Series)->float:
    if serie is None or serie.empty:
        return 0.0
    #contar os elementos: se tiver menos que 2 vendas não da para calcular o desvio padrão
    # divisão fica N=1 - 1 = 0
    if len(serie) < 2:
        return 0.0

    desvio = serie.std()

    #  Proteção caso todos os valores sejam iguais (o std() vira NaN)
    #A função len(serie) conta o tamanho físico da série, mesmo que os dados sejam nulos (None ou NaN).
    #pd.isna(desvio): Essa linha intercepta se o resultado da conta virou um NaN
    if pd.isna(desvio):
        return 0.0

    return float (desvio)


def calcular_variancia(serie: pd.Series) -> float:
    #barreira contra none e vazio
    if serie is None or serie.empty:
        return 0.0

    # Remove valores nulos E também remove preços iguais a 0 (se 0 for considerado inválido)
    serie_limpa = serie[(serie.notna() ) & (serie > 0)]

    #se houver só uma venda não dá para calcular a media e nem a variancia
    #tem uma pegadinha pode contar os produtos sem preço
    if len(serie_limpa) <2:
        return 0.0

    variancia = serie_limpa.var()

    #se a serie retorna nulo
    if pd.isna(variancia):
        return  0.0

    return float(variancia)

def calcular_quartis(serie: pd.Series) -> pd.Series:
    if serie is None or serie.empty:
        return pd.Series(dtype=float)

    serie_limpa = serie[(serie.notna()) & (serie > 0)]

    #Se após a limpeza não sobrou nenhum número válido
    if serie_limpa.empty:
        return pd.Series(dtype=float)

    return serie_limpa.quantile([0.25, 0.50, 0.75 ])





























"""def calcular_media(serie):
  serie_limpa = serie.dropna()
  if serie_limpa.empty:
    return 0.0
  return float(serie_limpa.mean())


def calcular_mediana(serie):
  serie_limpa = serie.dropna()
  if serie_limpa.empty:
    return 0.0
  return float(serie_limpa.median())


def calcular_moda(serie: pd.Series):
    serie_limpa = serie.dropna()
    if serie_limpa.empty:
        return None

    modas = serie_limpa.mode()
    if modas.empty:
        return None

    # Retorna o primeiro elemento caso haja mais de uma moda (empate)
    return modas.iloc[0]


def calcular_desvio_padrao(serie):
  # 1. Remove valores nulos da série do grupo
  serie_limpa = serie.dropna()

  # 2. Se o grupo tiver menos de 2 elementos, o desvio padrão é 0.0
  #produto vendeu apenas 1 vez não tem como tirar a media
  #Como só existe um valor de faturamento, ele é igual a si mesmo. Não existe dispersão, oscilação ou "distância da média".
  #O denominador da fórmula vira $1 - 1 .
  if len(serie_limpa) < 2:
    return 0.0

  return float(serie_limpa.std(ddof=1))


def calcular_variancia(serie: pd.Series) -> float:
    #ignorar os nulos
    variancia_valor = serie.var(ddof=1)
    if pd.isna(variancia_valor):
        return 0.0
    return float(variancia_valor)


def calcular_quartis(serie: pd.Series) -> pd.Series:
    return serie.quantile([0.25, 0.50, 0.75])"""
#Média
#Qual é o valor médio das vendas? Ajuda a avaliar o desempenho geral.

#Mediana
#Qual é o valor central das vendas? É útil quando existem pedidos excepcionalmente altos.

#Moda
#Qual valor aparece com maior frequência? Pode ajudar a identificar quantidades ou valores de venda recorrentes.

#Desvio padrão
#Quanto os valores variam em relação à média? Ajuda a avaliar a dispersão das vendas.

#Quartis
#Dividem os dados em quatro partes e ajudam a entender a distribuição das vendas e a
# identificar possíveis valores atípicos.

#   filtrado = df.loc[df['FATURAMENTO_LIQUIDO']>0, ['FATURAMENTO_LIQUIDO','ID-PRODUTO','PRODUTO']]
#    return filtrado['PRODUTO'].mode()