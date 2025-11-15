
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

st.title("🧠 Segmentación IA – Premium")

if "df" not in st.session_state:
    st.warning("Sube archivo.")
    st.stop()

df=st.session_state["df"]

seg_cols=["P25.  Edad ","P26. Género (opcional):","P28. Nivel de ingresos aproximado "]
seg_cols += [c for c in df.columns if c.startswith("P9") and "_rec" in c]

seg_df=df[seg_cols].fillna(0)
seg_df=pd.get_dummies(seg_df)

X=StandardScaler().fit_transform(seg_df)
labels=KMeans(n_clusters=5, random_state=42).fit_predict(X)

df["Segmento"]=labels

st.write("### Segmentos asignados:")
st.dataframe(df[["Segmento"]])

fig=px.histogram(df, x="Segmento", color="Segmento")
st.plotly_chart(fig)
