from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import json
import unicodedata

app = Dash(__name__)
server = app.server

# ======================
# NORMALIZAR TEXTO
# ======================
def normalizar(texto):
    if isinstance(texto, str):
        texto = texto.strip().lower()
        texto = ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )
    return texto

# ======================
# DATA
# ======================
df = pd.read_csv("data/escolaridad.csv")

df["estado"] = df["estado"].replace({
    "Coahuila de Zaragoza": "Coahuila",
    "Michoacán de Ocampo": "Michoacán",
    "Veracruz de Ignacio de la Llave": "Veracruz"
})

# ======================
# GEOJSON
# ======================
with open("data/mexico.json", encoding="utf-8") as f:
    geojson = json.load(f)

df["estado_norm"] = df["estado"].apply(normalizar)

for f in geojson["features"]:
    f["properties"]["name_norm"] = normalizar(f["properties"]["name"])

# ======================
# VARIABLES
# ======================
df = df.sort_values(by="escolaridad", ascending=True)

promedio = df["escolaridad"].mean()
df["diferencia"] = df["escolaridad"] - promedio

# ======================
# 1. PANORAMA
# ======================
fig1 = px.bar(
    df,
    x="escolaridad",
    y="estado",
    orientation="h",
    color="escolaridad",
    color_continuous_scale="Blues"
)

fig1.update_layout(height=900, margin=dict(l=200))
fig1.update_traces(marker_line_color="white", marker_line_width=1)

# ======================
# 2. BRECHA
# ======================
fig_diff = px.bar(
    df,
    x="diferencia",
    y="estado",
    orientation="h",
    color="diferencia",
    color_continuous_scale="RdBu"
)

fig_diff.add_vline(x=0, line_dash="dash", line_color="black")

# ======================
# 3. MAPA
# ======================
fig_map = px.choropleth(
    df,
    geojson=geojson,
    locations="estado_norm",
    featureidkey="properties.name_norm",
    color="escolaridad",
    color_continuous_scale="Blues"
)

fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_traces(marker_line_color="white", marker_line_width=1)

# ======================
# 4. EXPLORA TU ESTADO (CORREGIDA)
# ======================
def crear_fig_estado(estado):
    valor = df[df["estado"] == estado]["escolaridad"].values[0]
    
    # Color dinámico: Azul si está arriba/igual al promedio, Rojo si está por debajo
    color_estado = "#08519c" if valor >= promedio else "#b2182b"
    
    temp = pd.DataFrame({
        "Categoría": [estado, "Promedio Nacional"],
        "Valor": [valor, promedio]
    })

    fig = px.bar(
        temp,
        x="Categoría",
        y="Valor",
        color="Categoría",
        text="Valor",  # <--- EL CAMBIO CLAVE ESTÁ AQUÍ
        color_discrete_map={
            estado: color_estado,
            "Promedio Nacional": "#c2cce3"
        }
    )

    # Mejorar la apariencia de las barras y el texto
    fig.update_traces(
        texttemplate='<b>%{text:.2f}</b> años', # Ahora %{text} toma el valor correcto de cada barra
        textposition="outside",
        textfont_size=18,
        marker_line_color="white",
        marker_line_width=1.5
    )

    # Calcular la diferencia para mostrarla como subtítulo
    diff = valor - promedio
    if diff >= 0:
        texto_diff = f"<span style='color: #08519c;'><b>+{diff:.2f} años</b> por encima del promedio nacional</span>"
    else:
        # Se formatea en positivo para evitar el "--" ya que el texto dice "por debajo"
        texto_diff = f"<span style='color: #b2182b;'><b>{abs(diff):.2f} años</b> por debajo del promedio nacional</span>"

    # Limpieza visual profunda (sin eje Y, sin cuadrícula)
    fig.update_layout(
        template="plotly_white",
        height=450,
        title=dict(
            text=f"Comparativa de <b>{estado}</b><br><span style='font-size:15px'>{texto_diff}</span>",
            x=0.5,
            y=0.88,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        margin=dict(t=120, b=40, l=40, r=40),
        yaxis=dict(
            title="",
            showticklabels=False,  # Ocultar números del eje Y
            showgrid=False,        # Quitar la cuadrícula
            zeroline=False,
            range=[0, max(valor, promedio) * 1.25]  # Dar espacio extra arriba para el texto
        ),
        xaxis=dict(
            title="",
            showgrid=False,
            tickfont=dict(size=16, color="#333333")  # Nombres de las categorías más legibles
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",  # Fondo transparente
        paper_bgcolor="rgba(0,0,0,0)"  # Fondo transparente
    )

    return fig
# ======================
# LAYOUT
# ======================
app.layout = html.Div([

    # NAVBAR
    html.Div([
        html.Div("Brecha Educativa MX", style={"fontWeight": "bold"}),
        html.Div([
            html.A("Inicio", href="#inicio", className="nav-btn"),
            html.A("Panorama", href="#panorama", className="nav-btn"),
            html.A("Brecha", href="#brecha", className="nav-btn"),
            html.A("Mapa", href="#mapa", className="nav-btn"),
            html.A("Explorar", href="#explorar", className="nav-btn"),
        ], style={"display": "flex", "gap": "10px"})
    ], className="navbar"),

    html.Div([

        # INTRO
        html.H1("¿Dónde naces determina tu acceso a la educación?", id="inicio"),
        html.P(
            "Este análisis explora la desigualdad educativa en México a través de diferentes visualizaciones.",
            className="subtitle"
        ),

        # PANORAMA
        html.Div([
            html.H2("Panorama nacional", id="panorama"),
            html.P("Nivel educativo por estado.", className="text"),
            dcc.Graph(figure=fig1),
            html.P("Existen diferencias claras entre entidades.", className="text"),
        ], className="section"),

        # BRECHA
        html.Div([
            html.H2("Brecha educativa", id="brecha"),
            html.P("Diferencia respecto al promedio nacional.", className="text"),
            dcc.Graph(figure=fig_diff),
            html.P("Los valores negativos indican rezago.", className="text"),
        ], className="section"),

        # MAPA
        html.Div([
            html.H2("Distribución geográfica", id="mapa"),
            html.P("Dónde se concentra la desigualdad.", className="text"),
            dcc.Graph(figure=fig_map),
            html.P("El sur presenta menor escolaridad.", className="text"),
        ], className="section"),

        # EXPLORAR (MEJORADA)
        html.Div([
            html.H2("Explora tu estado", id="explorar"),
            html.P(
                "Selecciona un estado para compararlo con el promedio nacional.",
                className="text"
            ),

            dcc.Dropdown(
                id="estado-dropdown",
                options=[{"label": e, "value": e} for e in df["estado"]],
                value=df["estado"].iloc[0],
                style={"width": "60%", "margin": "auto"}
            ),

            html.Div([
                dcc.Graph(id="grafica-estado")
            ], style={
                "background": "white",
                "padding": "25px",
                "borderRadius": "15px",
                "boxShadow": "0px 10px 25px rgba(0,0,0,0.1)",
                "marginTop": "30px"
            })

        ], className="section"),

        # CONCLUSIÓN
        html.Div([
            html.H2("Conclusión"),
            html.P(
                "El lugar de nacimiento influye directamente en las oportunidades educativas en México."
            )
        ], className="conclusion-box")

    ], style={"padding": "40px"})

])

# ======================
# CALLBACK
# ======================
@app.callback(
    Output("grafica-estado", "figure"),
    Input("estado-dropdown", "value")
)
def update_graph(estado):
    return crear_fig_estado(estado)

# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(debug=True)