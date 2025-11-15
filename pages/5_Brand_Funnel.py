
import streamlit as st
import plotly.express as px

st.title("🍷 Brand Funnel – Visual Premium")

if "brand_funnel" not in st.session_state:
    st.warning("Cargue archivo Excel para ver el Brand Funnel.")
    st.stop()

bf = st.session_state["brand_funnel"]

st.write("### Brand Funnel Automático:")
st.dataframe(bf)

fig = px.bar(bf, title="Brand Funnel", labels={"index":"Marca","value":"Valor"})
st.plotly_chart(fig)
