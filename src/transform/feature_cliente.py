import numpy as np
import pandas as pd

def feature_cliente(df:pd.DataFrame)->pd.DataFrame:
    df = df.assign(
        TOTAL_GASTO_CLIENTE = lambda x: x.groupby('ID-CLIENTE')['FATURAMENTO_LIQUIDO'].transform('sum'),
        TOTAL_PEDIDOS_CLIENTE = lambda x: x.groupby('ID-CLIENTE')['ID-PEDIDO'].transform('nunique'),
        FATURAMENTO_CLIENTE_DEVOLVIDO = lambda x: x.groupby('ID-CLIENTE')['FATURAMENTO_LIQUIDO_DEVOLVIDO'].transform('sum'),

        TICKET_MEDIO_CLIENTE = lambda x:(
            np.where(
            x['TOTAL_PEDIDOS_CLIENTE'] > 0, np.round(x['TOTAL_GASTO_CLIENTE'] / x['TOTAL_PEDIDOS_CLIENTE'],2) ,0
            )
        )
    )

    return df

"""
feature_produto
├── FATURAMENTO_TOTAL_PRODUTOS
├── QTD_TOTAL_PRODUTOS
└── PRECO_MEDIO_LIQUIDO_PRODUTO

feature_pedido
├── FATURAMENTO_TOTAL_PEDIDOS
├── QTD_TOTAL_PEDIDO
└── VALOR_MEDIO_ITEM_PEDIDO

feature_cliente
├── TOTAL_GASTO_CLIENTE
├── TOTAL_PEDIDOS_CLIENTE
└── TICKET_MEDIO_CLIENTE
"""