import streamlit as st
import pandas as pd

st.title("🎨 Imagen y Asociaciones de Marca (P9)")

if "df" not in st.session_state:
    st.warning("Suba un archivo Excel primero.")
    st.stop()

df = st.session_state["df"]

p9_cols = [c for c in df.columns if c.startswith("P9")]

if p9_cols:
    st.write("### Tabla de atributos P9")
    st.dataframe(df[p9_cols])
else:
    st.warning("No se encontraron columnas P9 en el archivo cargado.")
