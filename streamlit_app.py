import streamlit as st
import pandas as pd

st.set_page_config(page_title="Investigación Kohlberg", layout="wide")

st.title("📊 Investigación de Mercado – Vinos Kohlberg")
st.subheader("Dashboard interactivo con carga de archivo Excel")

uploaded_file = st.file_uploader("📁 Subir archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.session_state["df"] = df
    st.success("✔ Archivo cargado correctamente")
    st.write("### Vista previa del dataset:")
    st.dataframe(df.head())
    st.info("Use el menú lateral para navegar por las páginas.")
else:
    st.warning("Suba un archivo Excel para comenzar.")
