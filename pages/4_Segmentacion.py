import streamlit as st
import plotly.express as px

st.title("🧠 Segmentación (IA)")

if "df" not in st.session_state:
    st.warning("Suba un archivo Excel primero.")
    st.stop()

df = st.session_state["df"]

if "Segmento" in df.columns:
    st.write("### Distribución de segmentos")
    st.bar_chart(df["Segmento"].value_counts())
else:
    st.warning("El archivo cargado no contiene la columna 'Segmento'.")
