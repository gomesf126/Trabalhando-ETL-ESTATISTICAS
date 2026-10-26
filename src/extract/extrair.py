import pandas as pd

from src.config.caminhos import DATA_RAW
from src.extract.logs import logging

logger = logging.getLogger(__name__)

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

def ler_arquivo(arquivo):
    try:
        logger.info(f"Carregando o arquivo {arquivo.name}")

        df = pd.read_csv(arquivo, sep=",")

        logger.info(f"Arquivo {arquivo.name} carregado com sucesso")

        return df

    except Exception as e:
        logger.error(f"Erro ao ler o arquivo {arquivo.name}: {e}")
        raise


def validar_coluna(df, arquivo):

    SCHEMA = [
        "id_pedido",
        "id_cliente",
        "id_produto",
        "categoria",
        "produto",
        "modelo",
        "nome",
        "sobrenome",
        "preco",
        "quantidade",
        "data",
        "loja"
    ]

    obrigatorias = set(SCHEMA)
    colunas_df   = set(df.columns)

    faltantes = obrigatorias - colunas_df
    extras    = colunas_df - obrigatorias

    if faltantes:
        raise ValueError(f"{arquivo.name}: colunas obrigatórias faltando: {faltantes}")

    if extras:
        logger.warning(f"Arquivo {arquivo.name} com colunas extras: {extras}")


def extrair_arquivo():

    tabelas = []

    try:
        arquivos = list(DATA_RAW.glob("*.csv"))

        if not arquivos:
            raise FileNotFoundError("Nenhum arquivo CSV encontrado")

        for arquivo in arquivos:

            df = ler_arquivo(arquivo)#função: read_csv

            validar_coluna(df, arquivo)

            tabelas.append(df)

        tabela = pd.concat(tabelas, ignore_index=True)

        logger.info(f"Total de arquivos lidos: {len(arquivos)}")
        logger.info(f"Total de linhas: {len(tabela)}")

        return tabela

    except Exception as e:
        logger.error(f"Erro ao extrair os arquivos: {e}")
        raise





