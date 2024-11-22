import streamlit as st
import pandas as pd
from  plotly import graph_objects as go


st.set_page_config(
    layout="wide",
    page_title="My Streamlit App",) 

st.title("Calculadora de inflación acumulada")
st.markdown("---")

tabla = pd.read_excel("inflacion.xlsx")
tabla['factor_inflacion'] = tabla.ipc/tabla.ipc.shift(1)
tabla['factor_inflacion'].fillna(1, inplace=True)

infla_anual = tabla.groupby('año')['factor_inflacion'].agg('prod').reset_index()
infla_anual['Inflacion_anual'] = ((infla_anual.factor_inflacion-1)*100).round(2)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=infla_anual['año'], 
    y=infla_anual['Inflacion_anual'], 
    mode='lines+markers',  
    name='Porcentaje por Año', 
    #line=dict(color='red', width=4),  # Línea roja, gruesa y semi-transparente
    #marker=dict(size=10, color='red',opacity = 0.9),
    hovertemplate='<br>Inflacion<br><b>%{x}:%{y}</b><br><br><extra></extra>' 
))

fig.update_traces(line=dict(shape='spline',color='coral', width=5),marker=dict(size=7, color='red',opacity = 0.6),opacity=.7)

# Ajustar el diseño del gráfico
fig.update_layout(
    title='Evolución de la inflación anual',  # Título del gráfico
    xaxis_title='Año',           # Título del eje X
    yaxis_title='Porcentaje (%)',
    yaxis=dict(
        dtick=20,
        ticksuffix='%', 
    ), 
    width=900,  
    height=600
)

c1,c2 = st.columns([2,1])

with c1:
    st.plotly_chart(fig)

with c2:
    st.write("")
    st.write("")
    with st.container(border=True):
        st.write('Al Principio')
        c1,c2,c3,c4 = st.columns([1,4,4,1])
        with c2:
            años_1 = tabla.año.unique()
            año_1 = st.selectbox("Año inicio",años_1)
            
        with c3:
            if año_1==1993:
                meses_1 = tabla.query('año==@año_1').mes.unique().tolist()
                del meses_1[0]
            else:
                meses_1= tabla.query('año==@año_1').mes.unique()
            mes_1 = st.selectbox("Mes inicio",meses_1)
            
        st.markdown("--- ---")
        st.write('Al final')
        col1,col2,col3,col4 = st.columns([1,4,4,1])
        with col2:
            año_2 = st.selectbox("Año final",años_1)
        with col3: 
            if año_1==1993:
                meses_2 = tabla.query('año==@año_2').mes.unique().tolist()
                del meses_2[0]
            else:
                meses_2 = tabla.query('año==@año_2').mes.unique()
            mes_2= st.selectbox("Mes final",meses_2)
        
        indice_filtro_1 = tabla.query("año==@año_1 & mes==@mes_1").index[0]
        indice_filtro_2 = tabla.query("año==@año_2 & mes==@mes_2").index[0]
        #ipc_inicio = tabla.query("año==@año_1 & mes==@mes_1").reset_index().ipc[0]

        ipc_inicio = tabla.loc[[indice_filtro_1-1]].reset_index().ipc[0]
        ipc_fin = tabla.query("año==@año_2 & mes==@mes_2").reset_index().ipc[0]
        inflacion_acumulada = (((ipc_fin/ipc_inicio)-1)*100).round(2)

        st.markdown("--- ---")  
        if indice_filtro_2<indice_filtro_1:
            st.error('¡Cuidado! La fecha inicial no puede ser mayor a la final.')
        else:
            st.subheader(f'Inflacion acumulada:{inflacion_acumulada}%')
        st.markdown("--- ---")
        
st.markdown("--- ---")
 
        

