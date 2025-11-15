
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import plotly.express as px

st.set_page_config(page_title="Kohlberg Insights", layout="wide")

st.markdown("""
<div style='text-align:center; padding:40px;'>
    <h1 style='color:#A40518; font-size:50px;'>🍷 Insights de Mercado – Vinos Kohlberg</h1>
    <h3 style='color:#CCCCCC;'>Dashboard Premium con IA y Visualizaciones Avanzadas</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.write("### 📁 Subir Base de Datos (Excel Original)")

uploaded = st.file_uploader("Sube tu archivo Excel:", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)
    st.success("✔ Archivo cargado correctamente")

    marca_map={1:"Kohlberg",2:"Aranjuez",3:"Campos de Solana",4:"Vinos Importados",12:"No recuerda / Otra"}

    cols_noto=[
        "P1. ¿Cuándo quiere comprar un vino qué marca es la primera que le viene a la mente?",
        "P1.1 Cuál la segunda marca? ",
        "P.1.2 Cúal la tercer marca ?"
    ]

    # Recodificación
    for c in cols_noto:
        if c in df.columns:
            df[c+"_rec"]=df[c].map(marca_map)

    p9_cols=[c for c in df.columns if c.startswith("P9")]
    for c in p9_cols:
        df[c+"_rec"]=df[c].map(marca_map)

    # Brand Funnel
    brands=list(marca_map.values())
    awareness={}
    for b in brands:
        awareness[b]=(
            (df[cols_noto[0]+"_rec"]==b) |
            (df[cols_noto[1]+"_rec"]==b) |
            (df[cols_noto[2]+"_rec"]==b)
        ).sum()

    bf = pd.DataFrame.from_dict(awareness, orient="index", columns=["Awareness"])
    df["P6_rec"]=df["P6.¿Cuál de estas marcas prefiere más? "].map(marca_map)
    df["P7_rec"]=df["P7. ¿Cuál diría que es la marca de vino que consume con mayor frecuencia?"].map(marca_map)

    bf["Preferencia"] = df["P6_rec"].value_counts()
    bf["Consumo"] = df["P7_rec"].value_counts()

    st.session_state["df"]=df
    st.session_state["brand_funnel"]=bf

    # Procesado descargable
    st.download_button(
        "⬇️ Descargar Excel Procesado",
        df.to_csv(index=False).encode("utf-8"),
        "base_procesada.csv",
        "text/csv"
    )

    st.write("### Vista previa:")
    st.dataframe(df.head())

else:
    st.warning("Por favor sube el archivo para comenzar.")
