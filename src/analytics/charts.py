
import src.analytics.metricas
import plotly.express as px
import streamlit as st

#função grafico é uma função generica onde ela recebe as funções gerar_metricas
#funçao grafico recebe alguns parametros como x , y e color para serem preenchidos "eixos"
#funcao_metrica, df, ano, x,y, color, title:str=None, eixox:str=None, eixoy:str=None
def grafico_bar(funcao_metrica, df, ano, x,y, color, title:str=None, eixox:str=None, eixoy:str=None):

    base = funcao_metrica(df ,  ano)
    fig = px.bar(
        base,
        y=y,
        x=x,
        color=color,
        orientation='h',
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(
        hovertemplate= f"<b> %{{y}} <b/>  <br>"
                       f" %{{x:,.2f}}  <br>"
                        "<extra></extra>",
        textposition='outside'
    )
    fig.update_layout(
        title=title if title else "Gráfico analítico",
        title_x=0.5,
        xaxis_title=eixox if eixox else "X",
        yaxis_title=eixoy if eixoy else "Y",
        template='plotly_white',
        showlegend=True
    )

    return fig




