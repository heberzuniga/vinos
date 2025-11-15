import streamlit as st
import plotly.express as px

st.title("📌 Notoriedad de Marca")

if "df" not in st.session_state:
    st.warning("Por favor suba un archivo Excel en la página principal.")
    st.stop()

df = st.session_state["df"]

cols = [
    "P1. ¿Cuándo quiere comprar un vino qué marca es la primera que le viene a la mente?",
    "P1.1 Cuál la segunda marca? ",
    "P.1.2 Cúal la tercer marca ?"
]

for c in cols:
    if c in df.columns:
        st.write(f"### Frecuencia de: {c}")
        fig = px.bar(df[c].value_counts(), title=c)
        st.plotly_chart(fig)
    else:
        st.error(f"Columna no encontrada: {c}")
