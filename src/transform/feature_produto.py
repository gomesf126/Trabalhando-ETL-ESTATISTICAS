import pandas as pd
import  numpy as np
from win32con import DF_ALLOWOTHERACCOUNTHOOK


#====================================================
#QUANTIDADE > 0  → venda
#QUANTIDADE = 0  → registro sem quantidade
#QUANTIDADE < 0  → possível devolução/cancelamento
#====================================================
def feature_produto(df:pd.DataFrame)-> pd.DataFrame:

    df['FATURAMENTO_LIQUIDO'] = df['PRECO'] * df['QUANTIDADE']
    df['FATURAMENTO_LIQUIDO_DEVOLVIDO'] = df['FATURAMENTO_LIQUIDO'].clip(upper=0).abs()
    df = df.assign(
        #isolar valores negativos (zerando/tirando) .. pega só os valores positivos
        QUANTIDADE_VENDIDA = lambda x: (x.groupby('ID-PRODUTO')['QUANTIDADE'].transform(lambda s: s.clip(lower=0).sum())),
        # isolar valores positivos (zerando/tirando).. pega os valores negativos e transforma em positivos
        QUANTIDADE_DEVOLVIDA = lambda x:(x.groupby('ID-PRODUTO')['QUANTIDADE'].transform(lambda s: s.clip(upper=0).abs().sum())),
        #QUANTIDADE LÍQUIDA
        QUANTIDADE_LIQUIDA = lambda x: x['QUANTIDADE_VENDIDA'] - x['QUANTIDADE_DEVOLVIDA'],


        #QUANTIDADE POR PRODUTO E POR PEDIDOS
        QTD_TOTAL_PRODUTOS = lambda x:(x.groupby('ID-PRODUTO')['QUANTIDADE'].transform('sum')),
        QTD_TOTAL_PEDIDO=lambda x: x.groupby('ID-PEDIDO')['QUANTIDADE'].transform('sum'),

        #FATURAMENTO TOTAL POR PRODUTO E POR PEDIDO
        FATURAMENTO_TOTAL_PEDIDOS =lambda x: x.groupby("ID-PEDIDO")["FATURAMENTO_LIQUIDO"].transform("sum"),
        FATURAMENTO_TOTAL_PRODUTOS = lambda x: x.groupby("ID-PRODUTO")["FATURAMENTO_LIQUIDO"].transform("sum"),
        FATURAMENTO_DEVOLVIDO_PRODUTO = lambda x: x.groupby('ID-PRODUTO')['FATURAMENTO_LIQUIDO_DEVOLVIDO'].transform('sum'),

        #TICKET MÉDIO POR PRODUTO OU POR PREÇO
        PRECO_MEDIO_LIQUIDO_PRODUTO = lambda x: np.where(
            x["QTD_TOTAL_PRODUTOS"] >= 0, np.round( x['FATURAMENTO_TOTAL_PRODUTOS'] / x['QTD_TOTAL_PRODUTOS'],2),0
            ),
        #TICKET MÉDIO POR PEDIDO OU POR VENDA
        TICKET_MEDIO_ITEM_PEDIDO = lambda x: np.where(
            x["QTD_TOTAL_PEDIDO"] >= 0,  np.round(x['FATURAMENTO_TOTAL_PEDIDOS'] / x['QTD_TOTAL_PEDIDO'],2),0
             )

    )

    df['TIPO_MOVIMENTO'] = np.select(
        [
                df['QUANTIDADE'] > 0,
                df['QUANTIDADE'] < 0,
                df['QUANTIDADE'] ==0
        ],
        [
                "VENDA", "DEVOLUÇÃO","SEM MOVIMENTO"
        ],"OUTRO"
    )

    return df


