
import streamlit as st

st.title("🍷 Brand Funnel Automático")

if "brand_funnel" not in st.session_state:
    st.warning("Debe cargar el archivo Excel.")
    st.stop()

st.dataframe(st.session_state["brand_funnel"])
