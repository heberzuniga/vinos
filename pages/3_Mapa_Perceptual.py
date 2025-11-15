
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS

st.title("🗺️ Mapa Perceptual – 2D y 3D Premium")

if "df" not in st.session_state:
    st.warning("Sube archivo.")
    st.stop()

df=st.session_state["df"]

p9_cols=[c for c in df.columns if c.startswith("P9") and "_rec" in c]
brands=["Kohlberg","Aranjuez","Campos de Solana","Vinos Importados"]

matrix=pd.DataFrame(index=brands)
for c in p9_cols:
    counts=df[c].value_counts()
    matrix[c]=[counts.get(b,0) for b in brands]

X=StandardScaler().fit_transform(matrix)
coords=MDS(n_components=2, random_state=42).fit_transform(X)

res=pd.DataFrame(coords, columns=["Dim1","Dim2"], index=brands)

fig2d=px.scatter(res, x="Dim1", y="Dim2", text=res.index, color=res.index, title="Mapa Perceptual 2D")
fig2d.update_traces(textposition="top center")
st.plotly_chart(fig2d)

# 3D
coords3d=MDS(n_components=3, random_state=42).fit_transform(X)
res3d=pd.DataFrame(coords3d, columns=["X","Y","Z"], index=brands)
fig3d=px.scatter_3d(res3d, x="X", y="Y", z="Z", text=res3d.index, color=res3d.index, title="Mapa Perceptual 3D")
st.plotly_chart(fig3d)

st.download_button(
    "⬇️ Descargar Coordenadas Mapa Perceptual",
    res.to_csv().encode("utf-8"),
    "mapa_perceptual.csv",
    "text/csv"
)
