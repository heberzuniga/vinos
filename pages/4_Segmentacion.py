
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.title("🧠 Segmentación IA – Premium (KMeans + KPIs)")

if "df" not in st.session_state:
    st.warning("Sube archivo primero.")
    st.stop()

df=st.session_state["df"]

seg_cols=["P25.  Edad ","P26. Género (opcional):","P28. Nivel de ingresos aproximado "]
seg_cols+=[c for c in df.columns if c.startswith("P9") and "_rec" in c]

seg_df=df[seg_cols].fillna(0)
seg_df=pd.get_dummies(seg_df)

X=StandardScaler().fit_transform(seg_df)
labels=KMeans(n_clusters=5, random_state=42).fit_predict(X)

df["Segmento"]=labels

st.write("### Distribución de segmentos")
fig=px.histogram(df, x="Segmento", color="Segmento")
st.plotly_chart(fig)

# KPIs
st.write("### 🟪 KPIs de Segmentación")
counts=df["Segmento"].value_counts()
for s in counts.index:
    st.metric(f"Segmento {s}", f"{counts[s]} personas")

st.download_button(
    "⬇️ Descargar Segmentación",
    df[["Segmento"]].to_csv().encode("utf-8"),
    "segmentacion.csv"
)
