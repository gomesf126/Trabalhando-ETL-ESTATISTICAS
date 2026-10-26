from src.pipeline.pipeline import pipeline
from src.extract.extrair import extrair_arquivo
from src.analytics.statistics import calcular_media,calcular_mediana,calcular_moda,calcular_quartis,calcular_variancia,calcular_desvio_padrao

from src.analytics.metricas import (
    gerar_metricas_com_moda,
    gerar_metricas_estatisticas_produto,
    gerar_metricas_estatisticas_geral,
    gerar_quartis_produto_ano

)

def main():

    df_raw = extrair_arquivo()
    df = df_raw.copy()
    df_final = pipeline(df)
    vendas = df_final.loc[ df_final['FATURAMENTO_LIQUIDO'] >0 , ['FATURAMENTO_LIQUIDO'] ]
    #print("Média:", calcular_media(vendas))
    #print("Mediana:", calcular_mediana(vendas))
    #print("Moda:", calcular_moda(vendas))
    #print("Desvio padrão:", calcular_desvio_padrao(vendas))
    #print("Quartis:")
    #print("Variancia", calcular_variancia(vendas))
    #print(calcular_quartis(vendas))
    #print(df_final.head(100))
    #print(df_final.columns)
    print(gerar_metricas_com_moda(df_final))
    print(gerar_metricas_estatisticas_produto(df_final))
    print(gerar_metricas_estatisticas_geral(df_final))
    print(gerar_quartis_produto_ano(df_final))
    #print(df_final.columns)

    return df_final



if __name__ ==  "__main__":
    df_final=main()
    #print(df_final)

