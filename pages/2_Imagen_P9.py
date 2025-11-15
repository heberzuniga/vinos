
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🎨 Imagen P9 – Premium (Radar, Heatmap, Barras)")

if "df" not in st.session_state:
    st.warning("Sube archivo primero.")
    st.stop()

df = st.session_state["df"]

p9_cols=[c for c in df.columns if c.startswith("P9") and "_rec" in c]
brands=["Kohlberg","Aranjuez","Campos de Solana","Vinos Importados"]

p9_matrix=pd.DataFrame(index=brands)

for c in p9_cols:
    counts=df[c].value_counts()
    p9_matrix[c]=[counts.get(b,0) for b in brands]

st.write("### 📊 Matriz perceptual")
st.dataframe(p9_matrix)

st.download_button(
    "⬇️ Descargar Matriz P9",
    p9_matrix.to_csv().encode("utf-8"),
    "p9_matrix.csv",
    "text/csv"
)

# Comparación por atributo
st.subheader("📊 Comparación por Atributo")
attr=st.selectbox("Selecciona atributo:", p9_cols)
fig1=px.bar(p9_matrix[attr], title=attr, color=p9_matrix[attr].index)
st.plotly_chart(fig1)

# Radar chart
st.subheader("🕸️ Radar Chart por Marca")
marca_sel=st.selectbox("Marca:", brands)

fig2=go.Figure()
fig2.add_trace(go.Scatterpolar(
    r=p9_matrix.loc[marca_sel].values,
    theta=p9_matrix.columns,
    fill='toself'
))
fig2.update_layout(title=f"Radar – {marca_sel}")
st.plotly_chart(fig2)

# Heatmap
st.subheader("🔥 Heatmap")
fig3=px.imshow(p9_matrix, color_continuous_scale="Reds")
st.plotly_chart(fig3)
