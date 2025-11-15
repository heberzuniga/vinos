
import streamlit as st

st.title("🎨 Imagen y Asociaciones – Visual Premium")

if "df" not in st.session_state:
    st.warning("Suba archivo.")
    st.stop()

df = st.session_state["df"]

p9 = [c for c in df.columns if "_rec" in c and c.startswith("P9")]
st.write("### Tabla de atributos P9:")
st.dataframe(df[p9])
