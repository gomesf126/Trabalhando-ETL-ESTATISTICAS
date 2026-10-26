import pandas as pd
import numpy  as np

def feature_churn_cliente(df:pd.DataFrame)->pd.DataFrame:
    data_atual = df['DATA'].max()
    df = df.assign(
        ULTIMA_COMPRA_CLIENTE = lambda x: x.groupby('ID-CLIENTE')['DATA'].transform('max'),
        DIAS_SEM_COMPRA       = lambda x: (data_atual - x['ULTIMA_COMPRA_CLIENTE']).dt.days
    ).assign(
        STATUS_COMPRA_CLIENTE = lambda x: np.select(
            [
                x['DIAS_SEM_COMPRA'] <= 30,
                x['DIAS_SEM_COMPRA'] <= 60,
                x['DIAS_SEM_COMPRA'] <= 90

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