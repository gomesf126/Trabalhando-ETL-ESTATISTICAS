
import plotly.express as px


def grafico_bar(funcao_metrica, df, ano, x,y, color,orientacao):

    base = funcao_metrica(df ,  ano)
    if orientacao.lower() == "v":
        fig = px.bar(
            base,
            x=y, # Categoria vai para o X no gráfico vertical
            y=x, # Valor numérico vai para o Y
            color=color,
            orientation='v',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        hovertemplate_str = "<b>%{x}</b><br>%{y:,.2f}<br><extra></extra>"

    else:
        fig = px.bar(
            base,
            x=y, # Categoria vai para o X no gráfico vertical
            y=x, # Valor numérico vai para o Y
            color=color,
            orientation='h',
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        hovertemplate_str = "<b>%{y}</b><br>%{x:,.2f}<br><extra></extra>"
    fig.update_traces(
        hovertemplate=  hovertemplate_str,
        textposition='outside'
    )
    fig.update_layout(
        #title=title if title else "Gráfico analítico",
        #title_x=0.5,
        xaxis_title= None,
        yaxis_title= None,
        template='plotly_white',
        showlegend=True,
        #bargap=0.15,  # Diminui o espaço entre as barras, deixando-as mais grossas
        #height=400 # Opcional: define uma altura fixa ideal para o container do Streamlit
    )

    return fig




