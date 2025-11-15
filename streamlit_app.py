
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
import plotly.express as px

st.set_page_config(page_title="Kohlberg Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;color:#A40518;'>📊 Investigación de Mercado – Vinos Kohlberg</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;color:#CCCCCC;'>Procesamiento Automático con IA + Visuales Premium</h3>", unsafe_allow_html=True)

uploaded = st.file_uploader("📁 Subir Excel original", type=["xlsx"],
                            help="Sube el archivo original para procesar todo automáticamente.")

if uploaded:
    df = pd.read_excel(uploaded)

    st.success("✔ Archivo cargado correctamente.")
    st.write("### Vista previa del dataset:")
    st.dataframe(df.head())

    # ---- RECODIFICACIÓN ----
    marca_map={1:"Kohlberg",2:"Aranjuez",3:"Campos de Solana",4:"Vinos Importados",12:"No recuerda / Otra"}
    cols_noto=[
        "P1. ¿Cuándo quiere comprar un vino qué marca es la primera que le viene a la mente?",
        "P1.1 Cuál la segunda marca? ",
        "P.1.2 Cúal la tercer marca ?"
    ]
    for c in cols_noto:
        if c in df.columns:
            df[c+"_rec"] = df[c].map(marca_map)

    # ---- P9 ----
    p9_cols=[c for c in df.columns if c.startswith("P9")]
    for c in p9_cols:
        df[c+"_rec"]=df[c].map(marca_map)

    # ---- Brand Funnel ----
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

    st.session_state["df"] = df
    st.session_state["brand_funnel"] = bf

else:
    st.warning("Suba el archivo Excel para habilitar el análisis.")
