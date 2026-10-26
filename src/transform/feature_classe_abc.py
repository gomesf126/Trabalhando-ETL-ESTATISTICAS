import pandas as pd
import numpy as np
def feature_classe_abc(df:pd.DataFrame)->pd.DataFrame:

    abc = (df
        [['ID-PRODUTO',
          'PRODUTO',
          'FATURAMENTO_LIQUIDO'
        ]]
            .drop_duplicates('ID-PRODUTO')
            .sort_values('FATURAMENTO_LIQUIDO', ascending=False)
            .reset_index(drop=True)
            .assign(
                percentual_produto = lambda x:
                x['FATURAMENTO_LIQUIDO'] / x['FATURAMENTO_LIQUIDO'].sum(),

                percentual_acumulado = lambda x: x['percentual_produto'].cumsum()
            )

        )
    abc['classe_abc'] = np.select(
        [
            abc['percentual_acumulado'] <= 0.80,
            abc['percentual_acumulado'] <= 0.95
        ],
        [
            'A','B'
        ],
        ['C']

    )
    return df.merge(
        abc[['ID-PRODUTO','percentual_produto','percentual_acumulado','classe_abc']],
        on= 'ID-PRODUTO', how='left'
    )