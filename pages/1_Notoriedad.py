
import streamlit as st
import plotly.express as px

st.title("📌 Notoriedad Automática")

if "df" not in st.session_state:
    st.warning("Suba un archivo primero.")
    st.stop()

df = st.session_state["df"]
cols = [c for c in df.columns if c.endswith("_rec") and c.startswith("P1")]

for c in cols:
    fig = px.bar(df[c].value_counts(), title=c)
    st.plotly_chart(fig)
