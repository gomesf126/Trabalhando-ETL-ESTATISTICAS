import pandas as pd
from src.config.caminhos import DATA_RAW
from src.extract.logs import logging
logger = logging.getLogger(__name__)

def validar_colunas(df, arquivo):
    SCHEMA = ['id_pedido','id_cliente','id_produto','categoria','produto','modelo','nome','sobrenome','preco','quantidade','data','loja']
    OBRIGATORIAS = set(SCHEMA)
    COLUNA_DF    = set(df.columns)

    coluna_faltante = OBRIGATORIAS - COLUNA_DF
    coluna_extra    = COLUNA_DF - OBRIGATORIAS

    if coluna_faltante:
        raise ValueError(f"{arquivo.name} Colunas obrigatorias faltantes: {coluna_faltante}")
    if coluna_extra:
        logger.warning(f"{arquivo.name}: Colunas extras {coluna_extra}")
    return df

def ler_arquivo(arquivo):
    try:
        logger.info(f"Lendo arquivo {arquivo.name}.")

        df=pd.read_csv(
            arquivo,
            sep=',')

        logger.info(f"Arquivos {arquivo.name} lidos com sucesso ")

        return df
    except Exception as erro:
        logger.error(f'Erro ao tentar ler o arquivo {arquivo.name}: {erro}')
        raise



def extract():
    tabelas = []
    try:
        arquivos = list(DATA_RAW.glob("*.csv"))
        if not arquivos:
            raise FileNotFoundError("Nenhum csv encontrado")

        for arquivo in arquivos:
            df = ler_arquivo(arquivo)
            validar_colunas(df,arquivo)
            tabelas.append(df)

        tabela = pd.concat(tabelas, ignore_index= True)

        logger.info(f"{len(tabelas)} Arquivos concatenadas.")
        logger.info(f"{len(tabela)} linhas totais")

        return tabela


    except Exception as erro:
        logger.error('Erro ao extrair o arquivo')
        raise

df =extract()
print(df.head(10))
print(df.columns)