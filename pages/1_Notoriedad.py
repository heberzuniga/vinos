
import streamlit as st
import plotly.express as px

st.title("📌 Notoriedad – Premium")

if "df" not in st.session_state:
    st.warning("Sube archivo primero.")
    st.stop()

df = st.session_state["df"]

cols = [c for c in df.columns if c.endswith("_rec") and c.startswith("P1")]

st.write("### Comparación de Notoriedad por Nivel")

for c in cols:
    fig = px.bar(df[c].value_counts(), title=c, color=df[c].value_counts().index)
    st.plotly_chart(fig)
