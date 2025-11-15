
import streamlit as st
import plotly.express as px

st.title("🍷 Brand Funnel – Premium")

if "brand_funnel" not in st.session_state:
    st.warning("Sube archivo primero.")
    st.stop()

bf = st.session_state["brand_funnel"]

st.dataframe(bf)

fig=px.bar(bf, labels={"index":"Marca","value":"Valor"})
st.plotly_chart(fig)
