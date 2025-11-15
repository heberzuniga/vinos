
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Kohlberg", layout="wide")

st.title("📊 Dashboard Principal – Vinos Kohlberg")
st.write("Sube tu archivo Excel para comenzar el análisis.")

archivo = st.file_uploader("📁 Sube tu archivo Excel (.xlsx)", type=["xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)
    st.success("Archivo cargado correctamente.")

    st.subheader("Vista previa de datos")
    st.dataframe(df.head())

    columnas = df.columns.tolist()

    st.markdown("---")

    st.subheader("⚙️ Configuración del Gráfico")

    tipo_grafico = st.selectbox(
        "Tipo de gráfico",
        ["Barras", "Histograma", "Dispersión", "Boxplot", "Mapa de calor"]
    )

    col1, col2 = st.columns(2)

    with col1:
        var_x = st.selectbox("Variable eje X:", columnas)

    with col2:
        var_y = st.selectbox("Variable eje Y (opcional):", ["(ninguna)"] + columnas)

    st.markdown("---")

    st.subheader("📈 Resultado")

    if tipo_grafico == "Barras":
        fig = px.bar(df, x=var_x, y=None if var_y == "(ninguna)" else df[var_y])
        st.plotly_chart(fig, use_container_width=True)

    elif tipo_grafico == "Histograma":
        fig = px.histogram(df, x=var_x)
        st.plotly_chart(fig, use_container_width=True)

    elif tipo_grafico == "Dispersión":
        if var_y == "(ninguna)":
            st.warning("Debes elegir una variable Y para un gráfico de dispersión.")
        else:
            fig = px.scatter(df, x=var_x, y=var_y)
            st.plotly_chart(fig, use_container_width=True)

    elif tipo_grafico == "Boxplot":
        fig = px.box(df, x=var_x, y=None if var_y == "(ninguna)" else df[var_y])
        st.plotly_chart(fig, use_container_width=True)

    elif tipo_grafico == "Mapa de calor":
        st.write("🔍 Mapa de calor basado en variables numéricas")
        df_numeric = df.select_dtypes(include="number")

        if df_numeric.empty:
            st.error("No hay columnas numéricas en el dataset.")
        else:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
