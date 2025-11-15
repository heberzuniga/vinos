
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import base64
import io
from sklearn.cluster import KMeans

df = pd.read_excel("data/BASE_DE_DATOS.xlsx")
df = df.convert_dtypes()
columnas = df.columns

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("Dashboard Profesional – Vinos Kohlberg",
            style={'textAlign':'center', 'color':'#800020'}),
    dcc.Tabs(id="tabs", value="tab-general", children=[
        dcc.Tab(label="Análisis General", value="tab-general"),
        dcc.Tab(label="Percepción de Marca (Radar)", value="tab-radar"),
        dcc.Tab(label="Nube de Palabras", value="tab-nube"),
        dcc.Tab(label="Publicidad y Medios", value="tab-publicidad"),
        dcc.Tab(label="Perfil del Consumidor", value="tab-perfil"),
        dcc.Tab(label="Clustering con IA", value="tab-cluster"),
        dcc.Tab(label="Mapa de Calor (Heatmap)", value="tab-heatmap"),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    Output("tabs-content", "children"),
    Input("tabs", "value")
)
def render_content(tab):
    if tab == "tab-general":
        return html.Div([
            html.H3("Gráfico Dinámico Interactivo"),
            html.Div([
                html.Div([
                    html.Label("Tipo de gráfico:"),
                    dcc.Dropdown(
                        id='tipo_grafico',
                        options=[
                            {'label': 'Barras', 'value': 'bar'},
                            {'label': 'Histograma', 'value': 'hist'},
                            {'label': 'Dispersión', 'value': 'scatter'},
                            {'label': 'Boxplot', 'value': 'box'},
                            {'label': 'Barras 100% apiladas', 'value': 'stack'},
                        ],
                        value='bar'
                    )
                ], style={'width':'30%', 'display':'inline-block'}),
                html.Div([
                    html.Label("Variable eje X:"),
                    dcc.Dropdown(
                        id='var_x',
                        options=[{'label': col, 'value': col} for col in columnas],
                        value=columnas[0]
                    )
                ], style={'width':'30%', 'display':'inline-block', 'marginLeft':'20px'}),
                html.Div([
                    html.Label("Variable eje Y (opcional):"),
                    dcc.Dropdown(
                        id='var_y',
                        options=[{'label': col, 'value': col} for col in columnas],
                        value=None
                    )
                ], style={'width':'30%', 'display':'inline-block', 'marginLeft':'20px'}),
            ]),
            dcc.Graph(id="grafico-general")
        ])

    elif tab == "tab-radar":
        return html.Div([
            html.H3("Radar Dinámico para Percepción de Marca"),
            html.Label("Selecciona variables (mínimo 3):"),
            dcc.Dropdown(
                id="radar-vars",
                options=[{'label': c, 'value': c} for c in columnas],
                value=columnas[:5],
                multi=True
            ),
            dcc.Graph(id="radar-grafico")
        ])

    elif tab == "tab-nube":
        return html.Div([
            html.H3("Nube de Palabras Interactiva"),
            html.Label("Columna con texto:"),
            dcc.Dropdown(
                id="nube-col",
                options=[{'label': c, 'value': c} for c in columnas],
                value=columnas[0]
            ),
            html.Img(id="nube-img", style={"width":"80%", "margin":"auto"})
        ])

    elif tab == "tab-publicidad":
        return html.Div([
            html.H3("Publicidad y Recordación – 100% Apilado"),
            html.Label("Variable publicitaria:"),
            dcc.Dropdown(
                id="publicidad-var",
                options=[{'label': c, 'value': c} for c in columnas],
                value=columnas[10]
            ),
            dcc.Graph(id="publicidad-graph")
        ])

    elif tab == "tab-perfil":
        return html.Div([
            html.H3("Perfil del Consumidor"),
            html.Label("Variable:"),
            dcc.Dropdown(
                id="perfil-var",
                options=[{'label': c, 'value': c} for c in columnas],
                value=columnas[2]
            ),
            dcc.Graph(id="perfil-graph")
        ])

    elif tab == "tab-cluster":
        return html.Div([
            html.H3("Clustering Automático (K-Means)"),
            html.Label("Variable X:"),
            dcc.Dropdown(
                id="cluster-x",
                options=[{'label': c, 'value': c} for c in columnas],
                value=columnas[0]
            ),
            html.Label("Variable Y:"),
            dcc.Dropdown(
                id="cluster-y",
                options=[{'label': c, 'value': c} for c in columnas],
                value=columnas[1]
            ),
            dcc.Graph(id="cluster-graph")
        ])

    elif tab == "tab-heatmap":
        return html.Div([
            html.H3("Mapa de Calor – Correlaciones"),
            dcc.Graph(id="heatmap-graph")
        ])

@app.callback(
    Output("grafico-general", "figure"),
    Input("tipo_grafico", "value"),
    Input("var_x", "value"),
    Input("var_y", "value")
)
def actualizar_general(tipo, x, y):
    if tipo == "bar":
        fig = px.bar(df, x=x, y=y, color=x)
    elif tipo == "hist":
        fig = px.histogram(df, x=x, color=x)
    elif tipo == "scatter":
        fig = px.scatter(df, x=x, y=y)
    elif tipo == "box":
        fig = px.box(df, x=x, y=y)
    elif tipo == "stack":
        fig = px.histogram(df, x=x, color=x, barnorm="percent")
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(
    Output("radar-grafico", "figure"),
    Input("radar-vars", "value")
)
def radar(v):
    if len(v) < 3:
        return go.Figure()
    valores = df[v].mean(numeric_only=True)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores.values,
        theta=valores.index,
        fill='toself'
    ))
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(
    Output("nube-img", "src"),
    Input("nube-col", "value")
)
def nube(col):
    texto = " ".join(df[col].dropna().astype(str))
    wc = WordCloud(width=1000, height=600, background_color="white").generate(texto)
    buf = io.BytesIO()
    wc.to_image().save(buf, format="PNG")
    data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{data}"

@app.callback(
    Output("publicidad-graph", "figure"),
    Input("publicidad-var", "value")
)
def publicidad(v):
    fig = px.histogram(df, x=v, color=v, barnorm="percent")
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(
    Output("perfil-graph", "figure"),
    Input("perfil-var", "value")
)
def perfil(v):
    fig = px.histogram(df, x=v, color=v)
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(
    Output("cluster-graph", "figure"),
    Input("cluster-x", "value"),
    Input("cluster-y", "value")
)
def cluster(x, y):
    df2 = df[[x, y]].dropna().astype(float)
    clusters = KMeans(n_clusters=3).fit_predict(df2)
    df2["Cluster"] = clusters
    fig = px.scatter(df2, x=x, y=y, color="Cluster")
    fig.update_layout(template="plotly_white")
    return fig

@app.callback(
    Output("heatmap-graph", "figure"),
    Input("tabs", "value")
)
def heatmap(_):
    df_num = df.select_dtypes(include=np.number)
    fig = px.imshow(df_num.corr(), text_auto=True, color_continuous_scale="RdBu_r")
    fig.update_layout(template="plotly_white")
    return fig

app.run_server(debug=True)
