
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS
import plotly.express as px

st.title("🗺️ Mapa Perceptual – Visual Premium")

if "df" not in st.session_state:
    st.warning("Suba archivo Excel.")
    st.stop()

df = st.session_state["df"]

p9_cols = [c for c in df.columns if c.startswith("P9") and "_rec" in c]
brands = ["Kohlberg","Aranjuez","Campos de Solana","Vinos Importados"]

matrix = pd.DataFrame(index=brands)
for c in p9_cols:
    counts = df[c].value_counts()
    matrix[c] = [counts.get(b,0) for b in brands]

X = StandardScaler().fit_transform(matrix)
coords = MDS(n_components=2, random_state=42).fit_transform(X)

result = pd.DataFrame(coords, columns=["Dim1","Dim2"], index=brands)

fig = px.scatter(result, x="Dim1", y="Dim2", text=result.index,
                 color=result.index,
                 title="Mapa Perceptual 2D")
fig.update_traces(textposition="top center")
st.plotly_chart(fig)
