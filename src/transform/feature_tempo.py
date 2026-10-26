import pandas as pd
def feature_tempo(df:pd.DataFrame)->pd.DataFrame:
    mes = {
        1: "jan",
        2: "fev",
        3: "mar",
        4: "abr",
        5: "mai",
        6: "jun",
        7: "jul",
        8: "ago",
        9: "set",
        10: "out",
        11: "nov",
        12: "dez"
    }
    df = df.assign(
        ANO = lambda x: x['DATA'].dt.year,
        MES_NUM =lambda x: x['DATA'].dt.month,
        MES = lambda x: x['DATA'].dt.month.map(mes)
    )


    return df

"""feature_tempo,
feature_churn,
feature_cliente,
feature_produto,
feature_financeiro,
feature_classe_abc"""



"""
df = df.assign(
    QUANTIDADE_VENDIDA=lambda x: (
        x.groupby('ID-PRODUTO')['QUANTIDADE']
         .transform(lambda s: s.clip(lower=0).sum())
    ),

    QUANTIDADE_DEVOLVIDA=lambda x: (
        x.groupby('ID-PRODUTO')['QUANTIDADE']
         .transform(lambda s: s.clip(upper=0).abs().sum())
    ),

    QTD_TOTAL_PRODUTOS=lambda x: (
        x.groupby('ID-PRODUTO')['QUANTIDADE']
         .transform('sum')
    ),

    FATURAMENTO_TOTAL_PEDIDOS=lambda x: (
        x.groupby('ID-PEDIDO')['FATURAMENTO_LIQUIDO']
         .transform('sum')
    ),

    FATURAMENTO_TOTAL_PRODUTOS=lambda x: (
        x.groupby('ID-PRODUTO')['FATURAMENTO_LIQUIDO']
         .transform('sum')
    ),

    TICKET_MEDIO_PRODUTO=lambda x: np.where(
        x['QTD_TOTAL_PRODUTOS'] != 0,
        np.round(
            x['FATURAMENTO_TOTAL_PRODUTOS']
            / x['QTD_TOTAL_PRODUTOS'],
            2
        ),
        0
    ),

    TICKET_MEDIO_PEDIDO=lambda x: np.where(
        x['QTD_TOTAL_PRODUTOS'] != 0,
        np.round(
            x['FATURAMENTO_TOTAL_PEDIDOS']
            / x['QTD_TOTAL_PRODUTOS'],
            2
        ),
        0
    )
)
"""