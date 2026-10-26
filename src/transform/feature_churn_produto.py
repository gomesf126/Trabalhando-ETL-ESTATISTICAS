import pandas as pd
import numpy as np
def feature_churn_produto(df:pd.DataFrame)->pd.DataFrame:
    data_atual = df['DATA'].max()

    df = df.assign(
        ULTIMA_VENDA = lambda x: x.groupby('ID-PRODUTO')['DATA'].transform('max'),
        DIAS_SEM_VENDA = lambda x: (data_atual - x['ULTIMA_VENDA']).dt.days
    ).assign(
        STATUS_VENDA = lambda x: np.select(
            [
                x['DIAS_SEM_VENDA'] <=30,
                x['DIAS_SEM_VENDA'] <= 60,
                x['DIAS_SEM_VENDA'] <= 90
            ],
            [
                "ATIVO",
                "ATENÇÃO",
                "RISCO"
            ],
            [
                "PERDIDO"
            ]
        )
    )

    return df