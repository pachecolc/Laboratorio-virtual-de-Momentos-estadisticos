from pathlib import Path
import re
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from models.estadistica import DATOS_PRESENTACION, aplicar_transformacion, resumen_estadistico, mascara_atipicos
from utils.exportacion import dataframe_a_excel

st.set_page_config(page_title="Momentos estadísticos",page_icon="📊",layout="wide")
ASSETS=Path("assets")

def encabezado():
    c1,c2=st.columns([5,1])
    with c1:
        st.title("📊 Momentos estadísticos y medidas descriptivas")
        st.caption("Laboratorio virtual: observar → predecir → modificar → simular → medir → registrar → interpretar")
    with c2:
        logo=ASSETS/"logo_serendipia.png"
        if logo.exists(): st.image(str(logo),width=120)
        else: st.caption("Logo pendiente")

def parsear_manual(txt):
    tokens=[t for t in re.split(r"[;\s]+",txt.strip()) if t]
    if not tokens: raise ValueError("Ingrese al menos dos valores separados por espacios, saltos de línea o punto y coma.")
    return np.array([float(t.replace(",",".")) for t in tokens],dtype=float)

def direccion(delta,tol=1e-10):
    return "permanece" if abs(delta)<=tol else ("aumenta" if delta>0 else "disminuye")

def figura_boxplot(x,titulo):
    fig=go.Figure(go.Box(x=x,name="Condición actual",boxpoints="all",jitter=0.28,pointpos=0))
    fig.update_layout(title=titulo,xaxis_title="Valor",template="plotly_white",height=340,showlegend=False,margin=dict(l=20,r=20,t=50,b=40))
    return fig

def figura_ordenada(x,res):
    y=np.sort(x); idx=np.arange(1,len(y)+1)
    fig=go.Figure(go.Scatter(x=idx,y=y,mode="lines+markers",name="Datos ordenados"))
    fig.add_hline(y=res["media"],line_dash="dash",annotation_text="Media")
    fig.add_hline(y=res["mediana"],line_dash="dot",annotation_text="Mediana")
    fig.update_layout(title="Datos ordenados",xaxis_title="Posición",yaxis_title="Valor",template="plotly_white",height=340,margin=dict(l=20,r=20,t=50,b=40))
    return fig

def figura_comparacion(ref,actual):
    fig=go.Figure()
    fig.add_trace(go.Box(x=ref,name="Referencia",boxpoints="outliers"))
    fig.add_trace(go.Box(x=actual,name="Actual",boxpoints="outliers"))
    fig.update_layout(title="Comparación de distribuciones",xaxis_title="Valor",template="plotly_white",height=360,margin=dict(l=20,r=20,t=50,b=40))
    return fig

def inicializar():
    if "datos_actuales" not in st.session_state: st.session_state.datos_actuales=DATOS_PRESENTACION.copy()
    if "datos_ref" not in st.session_state: st.session_state.datos_ref=DATOS_PRESENTACION.copy()
    if "meta" not in st.session_state: st.session_state.meta={"fuente":"Presentación","modo":"Sin transformación","escala":1.0,"desplazamiento":0.0,"factor_dispersion":1.0,"atipico":False,"valor_atipico":None}
    if "mediciones" not in st.session_state: st.session_state.mediciones=[]
    if "pred_guardada" not in st.session_state: st.session_state.pred_guardada={}

inicializar(); encabezado()

# ---------------- Sidebar: controles experimentales ----------------
st.sidebar.header("Controles experimentales")
fuente=st.sidebar.selectbox("Fuente de datos",["Datos de la presentación","Ingresar datos manualmente","Cargar CSV/TXT"])
base=None; fuente_nombre=fuente
if fuente=="Datos de la presentación": base=DATOS_PRESENTACION.copy()
elif fuente=="Ingresar datos manualmente":
    txt=st.sidebar.text_area("Valores",placeholder="10.2 9.8 11.1 ...",height=120)
    if txt.strip():
        try: base=parsear_manual(txt)
        except ValueError as e: st.sidebar.error(str(e))
else:
    up=st.sidebar.file_uploader("Archivo",type=["csv","txt"])
    if up is not None:
        try:
            df_up=pd.read_csv(up,sep=None,engine="python")
            num_cols=df_up.select_dtypes(include=np.number).columns.tolist()
            if not num_cols: st.sidebar.error("No se detectaron columnas numéricas.")
            else:
                col=st.sidebar.selectbox("Columna numérica",num_cols); base=df_up[col].dropna().to_numpy(dtype=float); fuente_nombre=f"{up.name} · {col}"
        except Exception as e: st.sidebar.error(f"No fue posible leer el archivo: {e}")

modo=st.sidebar.selectbox("Manipulación",["Sin transformación","Escala y desplazamiento","Dispersión con media constante"])
escala,desplazamiento,factor=1.0,0.0,1.0
if modo=="Escala y desplazamiento":
    escala=st.sidebar.slider("Factor de escala a",0.25,3.00,1.00,0.05)
    desplazamiento=st.sidebar.slider("Desplazamiento b",-10.0,10.0,0.0,0.5)
elif modo=="Dispersión con media constante": factor=st.sidebar.slider("Factor de dispersión k",0.25,3.00,1.00,0.05)
agregar_atipico=st.sidebar.checkbox("Agregar un valor extremo")
valor_atipico=st.sidebar.number_input("Valor extremo",value=30.0,step=1.0,disabled=not agregar_atipico)

st.sidebar.subheader("Predicción antes de simular")
pred_media=st.sidebar.selectbox("La media",["aumenta","disminuye","permanece","no sé"])
pred_var=st.sidebar.selectbox("La varianza",["aumenta","disminuye","permanece","no sé"])
just=st.sidebar.text_area("Justificación breve",height=80)

if st.sidebar.button("▶ Aplicar simulación",use_container_width=True):
    if base is None or len(base)<2: st.sidebar.error("Defina un conjunto con al menos dos observaciones.")
    else:
        try:
            actual=aplicar_transformacion(base,modo,escala,desplazamiento,factor,agregar_atipico,valor_atipico)
            st.session_state.datos_ref=np.asarray(base,dtype=float)
            st.session_state.datos_actuales=actual
            st.session_state.meta={"fuente":fuente_nombre,"modo":modo,"escala":escala,"desplazamiento":desplazamiento,"factor_dispersion":factor,"atipico":agregar_atipico,"valor_atipico":float(valor_atipico) if agregar_atipico else None}
            st.session_state.pred_guardada={"media":pred_media,"varianza":pred_var,"justificacion":just}
            st.sidebar.success("Simulación aplicada.")
        except ValueError as e: st.sidebar.error(str(e))
if st.sidebar.button("↺ Restablecer presentación",use_container_width=True):
    st.session_state.datos_ref=DATOS_PRESENTACION.copy(); st.session_state.datos_actuales=DATOS_PRESENTACION.copy()
    st.session_state.meta={"fuente":"Presentación","modo":"Sin transformación","escala":1.0,"desplazamiento":0.0,"factor_dispersion":1.0,"atipico":False,"valor_atipico":None}; st.session_state.pred_guardada={}

x=st.session_state.datos_actuales; ref=st.session_state.datos_ref
r=resumen_estadistico(x); rr=resumen_estadistico(ref); meta=st.session_state.meta

tabs=st.tabs(["🔎 Explorar","⚖️ Comparar","🧮 Modelo y cálculo manual","🧪 Experimentos guiados","🗂 Registro"])
with tabs[0]:
    st.subheader("Resultado de la condición actual")
    c=st.columns(4); c[0].metric("n",r["n"]); c[1].metric("Media",f"{r['media']:.3f}"); c[2].metric("Varianza σ²",f"{r['varianza']:.3f}"); c[3].metric("Desv. estándar σ",f"{r['desv_std']:.3f}")
    c=st.columns(4); c[0].metric("Mediana",f"{r['mediana']:.3f}"); c[1].metric("Q1",f"{r['q1']:.3f}"); c[2].metric("Q3",f"{r['q3']:.3f}"); c[3].metric("Atípicos (1.5·IQR)",r["n_atipicos"])
    a,b=st.columns(2); a.plotly_chart(figura_ordenada(x,r),use_container_width=True); b.plotly_chart(figura_boxplot(x,"Boxplot de la condición actual"),use_container_width=True)
    with st.expander("Interpretación automática",expanded=True):
        if r["desv_std"]>0:
            dif=abs(r["media"]-r["mediana"])/r["desv_std"]
            texto="muy próximas" if dif<0.10 else "separadas de forma apreciable"
        else: texto="idénticas porque no hay dispersión"
        st.write(f"La media y la mediana están **{texto}**. El rango intercuartílico es **{r['iqr']:.3f}** y la regla 1.5·IQR identifica **{r['n_atipicos']}** valor(es) atípico(s).")
        st.write("Este resumen describe centro y dispersión; por sí solo no demuestra normalidad ni causalidad.")
    st.caption(f"Fuente: {meta['fuente']} · Manipulación: {meta['modo']}")

with tabs[1]:
    st.subheader("Referencia vs condición simulada")
    comp=pd.DataFrame({
        "Medida":["n","Media","Varianza","Desv. estándar","Mediana","Q1","Q3","IQR","Atípicos"],
        "Referencia":[rr["n"],rr["media"],rr["varianza"],rr["desv_std"],rr["mediana"],rr["q1"],rr["q3"],rr["iqr"],rr["n_atipicos"]],
        "Actual":[r["n"],r["media"],r["varianza"],r["desv_std"],r["mediana"],r["q1"],r["q3"],r["iqr"],r["n_atipicos"]]
    })
    comp["Cambio"]=pd.to_numeric(comp["Actual"],errors="coerce")-pd.to_numeric(comp["Referencia"],errors="coerce")
    st.dataframe(comp,use_container_width=True,hide_index=True); st.plotly_chart(figura_comparacion(ref,x),use_container_width=True)
    pm=st.session_state.pred_guardada
    if pm:
        obs_m=direccion(r["media"]-rr["media"]); obs_v=direccion(r["varianza"]-rr["varianza"])
        st.markdown("**Contraste de la predicción**")
        st.write(f"Media: predicción **{pm['media']}** → observado **{obs_m}**. Varianza: predicción **{pm['varianza']}** → observado **{obs_v}**.")
        if pm.get("justificacion"): st.caption("Justificación registrada: "+pm["justificacion"])

with tabs[2]:
    st.subheader("Modelo descriptivo implementado")
    st.latex(r"\bar{x}=\frac{1}{N}\sum_{i=1}^{N}x_i")
    st.latex(r"\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\bar{x})^2")
    st.latex(r"\sigma=\sqrt{\sigma^2}")
    st.latex(r"IQR=Q_3-Q_1,\qquad [Q_1-1.5IQR,\;Q_3+1.5IQR]")
    st.info("La varianza se calcula como varianza poblacional (ddof=0), igual que en el código de la presentación. Q1 y Q3 se calculan con NumPy mediante percentiles 25 y 75.")
    st.markdown("**Cálculo manual vs simulador**")
    c1,c2=st.columns(2)
    manual_media=c1.number_input("Media calculada manualmente",value=0.0,format="%.6f")
    manual_var=c2.number_input("Varianza calculada manualmente",value=0.0,format="%.6f")
    if st.button("Comparar cálculo manual"):
        rows=[]
        for nombre,manual,sim in [("Media",manual_media,r["media"]),("Varianza",manual_var,r["varianza"])]:
            dif=manual-sim; err=abs(dif/sim)*100 if sim!=0 else np.nan
            rows.append({"Medida":nombre,"Valor manual":manual,"Simulador":sim,"Diferencia":dif,"% error":err})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

with tabs[3]:
    st.subheader("Secuencia experimental sugerida")
    st.markdown("""
**Experimento 1 — Condición basal.** Seleccione *Datos de la presentación*, *Sin transformación* y sin valor extremo. Prediga, simule, registre y describa centro y dispersión.

**Experimento 2 — Traslación.** Seleccione *Escala y desplazamiento*, use `a = 1.00` y `b = +3.0`. Antes de simular, prediga qué medidas cambian y cuáles permanecen.

**Experimento 3 — Misma media, distinta dispersión.** Seleccione *Dispersión con media constante* y `k = 2.00`. Compare media, varianza, desviación estándar y boxplot con la referencia.

**Experimento 4 — Sensibilidad a un valor extremo.** Regrese a *Sin transformación*, active *Agregar un valor extremo* y use `30`. Compare cuánto cambian la media y la mediana; observe el boxplot.

**Experimento 5 — Escalamiento.** Use *Escala y desplazamiento* con `a = 2.00` y `b = 0`. Explique el efecto sobre centro y dispersión.

**Experimento libre.** Diseñe una manipulación propia, formule una hipótesis antes de simular y justifique el resultado.
""")
    st.warning("Cambie una sola variable por experimento cuando el objetivo sea establecer una relación causa–efecto descriptiva.")

with tabs[4]:
    st.subheader("Registro experimental")
    c1,c2=st.columns(2)
    if c1.button("➕ Registrar medición",use_container_width=True):
        m=st.session_state.meta; p=st.session_state.pred_guardada
        st.session_state.mediciones.append({
            "Experimento":len(st.session_state.mediciones)+1,"Fuente":m["fuente"],"Manipulación":m["modo"],
            "Escala a":m["escala"],"Desplazamiento b":m["desplazamiento"],"Factor k":m["factor_dispersion"],
            "Valor extremo":m["valor_atipico"],"n":r["n"],"Media":r["media"],"Varianza":r["varianza"],
            "Desv. estándar":r["desv_std"],"Mediana":r["mediana"],"Q1":r["q1"],"Q3":r["q3"],"IQR":r["iqr"],
            "N atípicos":r["n_atipicos"],"Pred. media":p.get("media",""),"Pred. varianza":p.get("varianza","")
        })
        st.success("Medición registrada.")
    if c2.button("🗑 Borrar todas las mediciones",use_container_width=True): st.session_state.mediciones=[]; st.rerun()
    if st.session_state.mediciones:
        df=pd.DataFrame(st.session_state.mediciones); st.dataframe(df,use_container_width=True,hide_index=True)
        d1,d2=st.columns(2)
        d1.download_button("Descargar CSV",df.to_csv(index=False).encode("utf-8"),"experimentos_momentos_estadisticos.csv","text/csv",use_container_width=True)
        d2.download_button("Descargar Excel",dataframe_a_excel(df),"experimentos_momentos_estadisticos.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
    else: st.info("Aún no hay mediciones registradas.")

st.divider(); st.caption("Simulador educativo. Las transformaciones son manipulaciones didácticas de un conjunto de datos y no sustituyen el análisis del contexto experimental original.")
