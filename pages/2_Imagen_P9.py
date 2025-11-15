
import streamlit as st

st.title("🎨 Imagen P9 (procesada automáticamente)")

if "df" not in st.session_state:
    st.warning("Suba un archivo.")
    st.stop()

df = st.session_state["df"]
p9 = [c for c in df.columns if "_rec" in c and c.startswith("P9")]
st.dataframe(df[p9])
