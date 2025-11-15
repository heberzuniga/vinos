import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🎨 Imagen y Asociaciones de Marca (P9) – Visual Premium")

if "df" not in st.session_state:
    st.warning("Suba un archivo Excel primero.")
    st.stop()

df = st.session_state["df"]

p9_cols = [c for c in df.columns if c.startswith("P9") and "_rec" in c]

if len(p9_cols) == 0:
    st.error("No se encontraron columnas P9 recodificadas.")
    st.stop()

st.write("### 📌 Matriz de asociaciones (conteo por atributo y marca)")

brands = ["Kohlberg", "Aranjuez", "Campos de Solana", "Vinos Importados"]
p9_matrix = pd.DataFrame(index=brands)

for c in p9_cols:
    counts = df[c].value_counts()
    p9_matrix[c] = [counts.get(b, 0) for b in brands]

st.dataframe(p9_matrix)

st.subheader("📊 Comparación por Atributo")
attr = st.selectbox("Selecciona un atributo:", p9_cols)

fig1 = px.bar(
    p9_matrix[attr],
    title=f"Asociación por Marca – {attr}",
    labels={"value": "Frecuencia", "index": "Marca"},
    color=p9_matrix[attr].index,
)
st.plotly_chart(fig1)

st.subheader("🕸️ Perfil Perceptual (Radar Chart)")
marca_sel = st.selectbox("Selecciona una marca:", brands)

fig2 = go.Figure()
fig2.add_trace(go.Scatterpolar(
    r=p9_matrix.loc[marca_sel].values,
    theta=p9_matrix.columns,
    fill='toself',
    name=marca_sel
))
fig2.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    title=f"Radar Chart – Perfil perceptual de {marca_sel}",
    showlegend=False,
)
st.plotly_chart(fig2)

st.subheader("🔥 Heatmap de Percepciones (Fuerzas y Debilidades)")
fig3 = px.imshow(
    p9_matrix,
    labels=dict(x="Atributo", y="Marca", color="Frecuencia"),
    x=p9_matrix.columns,
    y=p9_matrix.index,
    color_continuous_scale="Reds",
    title="Mapa de Calor – Matriz P9"
)
st.plotly_chart(fig3)
