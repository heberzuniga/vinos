
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

st.title("🧠 Segmentación Automática")

if "df" not in st.session_state:
    st.warning("Suba archivo Excel.")
    st.stop()

df = st.session_state["df"]

seg_cols = ["P25.  Edad ","P26. Género (opcional):","P28. Nivel de ingresos aproximado "] + \
           [c for c in df.columns if c.startswith("P9") and "_rec" in c]

seg_df = df[seg_cols].fillna(0)
seg_df = pd.get_dummies(seg_df)

X = StandardScaler().fit_transform(seg_df)
labels = KMeans(n_clusters=5, random_state=42).fit_predict(X)

df["Segmento"] = labels
st.dataframe(df[["Segmento"]])

fig = px.histogram(df, x="Segmento", title="Distribución de Segmentos")
st.plotly_chart(fig)
