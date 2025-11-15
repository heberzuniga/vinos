
import streamlit as st
import plotly.express as px

st.title("🍷 Brand Funnel Premium")

if "brand_funnel" not in st.session_state:
    st.warning("Sube archivo primero.")
    st.stop()

bf=st.session_state["brand_funnel"]

st.write("### Brand Funnel")
st.dataframe(bf)

fig=px.bar(bf, title="Brand Funnel (Awareness–Preferencia–Consumo)")
st.plotly_chart(fig)

st.download_button(
    "⬇️ Descargar Brand Funnel",
    bf.to_csv().encode("utf-8"),
    "brand_funnel.csv",
    "text/csv"
)
