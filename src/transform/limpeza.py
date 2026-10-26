from base64 import decode, encode
from src.extract.extrair import extrair_arquivo
import pandas as pd
import unicodedata
import numpy as np
def padronizar_colunas(df:pd.DataFrame)->pd.DataFrame:
    df.columns = [
         unicodedata.normalize("NFKD",col)#separar o caractere da sua acentuação "J" "o" "a" + acento "˜" "o"
        .encode("ascii","ignore")#remova os caracteres que não pertencem ao ASCII
        .decode("utf-8")#decode("utf-8")transforma os bytes novamente em texto.
        for col in df.columns
    ]

    df.columns=(
            df.columns
            .str.strip()
            .str.upper()
            .str.replace("_", "-")
        )
    df = df.iloc[:,~df.columns.str.contains('^ARQUIVO-ORIGEM', case=False)]
    return df

#ok
def padronizar_texto(df:pd.DataFrame)->pd.DataFrame:
    padrao_coluna = df.select_dtypes(include=['str', 'object']).columns
    for col in padrao_coluna:
        df[col] = (
            df[col].astype(str)
            .str.strip()
            .str.upper()
        )
    return df

#ok
def padronizar_preco_quantidade(df:pd.DataFrame)->pd.DataFrame:
    col_numericos = ['QUANTIDADE','PRECO']
    col_numero =[
         col for col in col_numericos
         if col in df.columns
    ]
    for col in col_numero:
        limpa = (  df[col]
                    .astype(str)#BR" R$ 1.250,50" EUA "$ 1,250.50"
                    .str.replace(r'[^\d.-]','', regex=True)#tira duto e mantem só numeros a virgula e o - ..trata o milhar
                    .str.strip()
                 )
        df[col] = pd.to_numeric(limpa, errors='coerce')


    if 'QUANTIDADE' in df.columns:
        df['QUANTIDADE']= df['QUANTIDADE'].astype('Int64')

    return df

#ok
def padronizar_datas(df:pd.DataFrame)->pd.DataFrame:
    df['DATA']=  pd.to_datetime(df['DATA'], errors='coerce', dayfirst=False)
    df['DATA_BR'] = df['DATA'].dt.strftime('%d/%m/%Y')
    return df

#ok
def sinalizar_negativos(df:pd.DataFrame)->pd.DataFrame:

    df['QUANTIDADE_NEGATIVA'] = df['QUANTIDADE'] < 0
    df['PRECO_NEGATIVO'] = df['PRECO'] < 0

    mediana = df.loc[df['PRECO'] >=0 , 'PRECO'].median()

    df['PRECO'] = np.where(
        df['PRECO'] <0, mediana, df['PRECO']
    )
    return df

#ok
def tratar_nulos(df:pd.DataFrame)->pd.DataFrame:
    dados   =['CATEGORIA', 'PRODUTO','MODELO', 'NOME','SOBRENOME', 'LOJA']
    numeros = ['PRECO', 'QUANTIDADE']

    for col in dados:
        if col in df.columns:
            df[col]=df[col].fillna('Dado ausente')
    if 'DATA_BR' in df.columns:
        df['DATA_BR'] = df['DATA_BR'].fillna("Data ausente")

    for col in numeros:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df



#ok
def tratar_duplicatas(df:pd.DataFrame)->pd.DataFrame:
    return df.drop_duplicates()

#ok
def validar_tipos_dados(df:pd.DataFrame)->pd.DataFrame:
    dados = pd.DataFrame(
        [
            {
            "Colunas": df.columns.tolist(),
            "Tipo_Dados": df.dtypes.astype(str).values
            }
        ]
    )
    return dados
    #ok

#ok
def dados_duplicados(df:pd.DataFrame)->pd.DataFrame:
    total_linhas = len(df)
    duplicados = df.duplicated().sum()
    percent = round( (duplicados / total_linhas * 100),2 )  if total_linhas > 0 else 0

    dados =pd.DataFrame(
        [
            {
            'Quantidade_de_linhas' : total_linhas,
            'Duplicados'           : duplicados,
            'Percentual_duplicados': percent
            }
        ]
    )
    return dados

def gerar_relatorio_diagnostico(df:pd.DataFrame):
    tipos = validar_tipos_dados(df)
    duplicados = dados_duplicados(df)
    return tipos, duplicados


#"Utilizo o .copy() no início do pipeline para garantir imutabilidade e isolamento de dados.



"""
Formato Brasileiro (BR) para Pandas
Lida com valores no padrão R$ 1.250,50. Mantém a vírgula, elimina o ponto de milhar e converte a vírgula para ponto.

def padronizar_br_para_pandas(df: pd.DataFrame) -> pd.DataFrame:
    col_numericos = ["QUANTIDADE", "PRECO"]
    col_numero = [col for col in col_numericos if col in df.columns]

    for col in col_numero:
        limpa = (
            df[col]
            .astype(str)
            .str.replace(
                r"[^\d,-]", "", regex=True
            )  # Remove ponto de milhar e símbolos, mantém a vírgula
            .str.replace(",", ".", regex=False)  # Troca vírgula por ponto
            .str.strip()
        )
        df[col] = pd.to_numeric(limpa, errors="coerce")

    if "QUANTIDADE" in df.columns:
        df["QUANTIDADE"] = df["QUANTIDADE"].astype("Int64")

    return df"""

"""import pandas as pd
Formato Americano (US) para Pandas
Lida com valores no padrão $ 1,250.50 ou 6542.08. Mantém o ponto decimal e elimina as vírgulas de milhar.

def padronizar_us_para_pandas(df: pd.DataFrame) -> pd.DataFrame:
    col_numericos = ["QUANTIDADE", "PRECO"]
    col_numero = [col for col in col_numericos if col in df.columns]

    for col in col_numero:
        limpa = (
            df[col]
            .astype(str)
            .str.replace(
                r"[^\d.-]", "", regex=True
            )  # Remove vírgula de milhar e símbolos, mantém o ponto
            .str.strip()
        )
        df[col] = pd.to_numeric(limpa, errors="coerce")

    if "QUANTIDADE" in df.columns:
        df["QUANTIDADE"] = df["QUANTIDADE"].astype("Int64")

    return df"""