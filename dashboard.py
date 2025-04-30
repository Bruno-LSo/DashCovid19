import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import json

# === Data Load & Preprocessing ===
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")

# converter coluna de data e remover colunas não usadas
df_states["data"] = pd.to_datetime(df_states["data"])
df_brasil["data"] = pd.to_datetime(df_brasil["data"])

to_drop = [
    "municipio", "codmun",
    "codRegiaoSaude", "nomeRegiaoSaude", "interior/metropolitana"
]
df_states.drop(columns=to_drop, inplace=True)
df_brasil.drop(columns=to_drop, inplace=True)

# carregar geojson dos estados
with open("geojson/brazil_geo.json", "r") as f:
    brazil_states = json.load(f)

select_columns = {
    "casosAcumulado":   "Casos Acumulados",
    "casosNovos":       "Novos Casos",
    "obitosAcumulado":  "Óbitos Totais",
    "obitosNovos":      "Óbitos por dia"
}

# lista de anos disponíveis
anos_disponiveis = sorted(df_states["data"].dt.year.unique())
year_options = [{"label": "Todos", "value": "ALL"}] + [
    {"label": str(y), "value": y} for y in anos_disponiveis
]

# data inicial para mapa
initial_date = df_states["data"].max()

# =====================================================================
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# mapa inicial
df_init = df_states[df_states["data"] == initial_date]
fig_map = px.choropleth_map(
    df_init, geojson=brazil_states, locations="estado", color="casosNovos",
    color_continuous_scale="Redor", opacity=0.5,
    hover_data=["casosAcumulado", "casosNovos", "obitosNovos"],
    zoom=4, center={"lat": -14.5, "lon": -52.0}, map_style="carto-darkmatter"
)
fig_map.update_layout(
    paper_bgcolor="#242424",
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False
)

# placeholder para gráfico de linha
fig_line = go.Figure(layout={"template": "plotly_dark"})

# === Layout ===
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # coluna esquerda: controles e gráficos
        dbc.Col(md=5, style={"padding":"25px","background-color":"#242424"}, children=[
            # cabeçalho
            html.Div(style={"background-color":"#1E1E1E","margin":"-25px","padding":"25px"}, children=[
                html.Div(style={"display":"flex","alignItems":"center"}, children=[
                    html.Img(id="logo", src=app.get_asset_url("logo_dark.png"), height=50),
                    html.Span("Desenvolvido por BLS", style={"marginLeft":"10px","color":"#FFF","fontSize":"16px"})
                ]),
                html.H2("Evolução da COVID-19 no Brasil de 2020 a 2025"),
                html.H6("Fonte: https://covid.saude.gov.br/"),
                dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
            ]),

            # filtro por ano
            html.P("Selecione o ano:", style={"margin-top":"20px","color":"#FFF"}),
            dcc.Dropdown(
                id="year-dropdown",
                options=year_options,
                value=["ALL"],
                multi=True,
                clearable=False,
                style={"background-color":"#1E1E1E","color":"#FFF"}
            ),

            # date picker
            html.P("Informe a data:", style={"margin-top":"40px","color":"#FFF"}),
            dcc.DatePickerSingle(
                id="date-picker",
                min_date_allowed=df_states["data"].min(),
                max_date_allowed=df_states["data"].max(),
                initial_visible_month=df_states["data"].max(),
                date=df_states["data"].max(),
                display_format="DD/MM/YYYY",
                style={"border":"0px","color":"#FFF"}
            ),

            # cards de resumo
            dbc.Row([
                dbc.Col(md=4, children=dbc.Card(dbc.CardBody([
                    html.Span("Casos recuperados"),
                    html.H3(id="casos-recuperados-text", style={"color":"#adfc92"}),
                    html.Span("Em acompanhamento"),
                    html.H5(id="em-acompanhamento-text")
                ]), color="light", outline=True, style={"margin-top":"10px","color":"#FFF"})),
                dbc.Col(md=4, children=dbc.Card(dbc.CardBody([
                    html.Span("Casos totais"),
                    html.H3(id="casos-confirmados-text", style={"color":"#389fd6"}),
                    html.Span("Novos casos na data"),
                    html.H5(id="novos-casos-text")
                ]), color="light", outline=True, style={"margin-top":"10px","color":"#FFF"})),
                dbc.Col(md=4, children=dbc.Card(dbc.CardBody([
                    html.Span("Óbitos totais"),
                    html.H3(id="obitos-text", style={"color":"#DF2935"}),
                    html.Span("Óbitos na data"),
                    html.H5(id="obitos-na-data-text")
                ]), color="light", outline=True, style={"margin-top":"10px","color":"#FFF"})),
            ], style={"margin-top":"20px"}),

            # série temporal
            html.Div(style={"margin-top":"25px"}, children=[
                html.P("Selecione o indicador:", style={"color":"#FFF"}),
                dcc.Dropdown(
                    id="location-dropdown",
                    options=[{"label": lbl, "value": val} for val, lbl in select_columns.items()],
                    value="casosNovos",
                    clearable=False,
                    style={"background-color":"#1E1E1E","color":"#FFF"}
                ),
                dcc.Graph(id="line-graph", figure=fig_line, style={"background-color":"#242424"})
            ]),

            # comparar dois estados
            html.Div(style={"padding":"15px","background-color":"#1E1E1E","margin-top":"20px"}, children=[
                html.H6("Comparar dois estados:", style={"color":"#FFF"}),
                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        id="state1-dropdown",
                        options=[{"label": s, "value": s} for s in sorted(df_states["estado"].unique())],
                        value="SP",
                        clearable=False
                    ), md=6),
                    dbc.Col(dcc.Dropdown(
                        id="state2-dropdown",
                        options=[{"label": s, "value": s} for s in sorted(df_states["estado"].unique())],
                        value="RJ",
                        clearable=False
                    ), md=6),
                ], style={"margin-bottom":"10px"}),
                html.Div(id="compare-text", style={"color":"#FFF"}),
                dcc.Graph(id="compare-graph", style={"height":"300px","background-color":"#242424"})
            ]),
        ]),

        # coluna direita: mapa
        dbc.Col(md=7, children=[
            dcc.Loading(
                id="loading-1",
                type="default",
                children=dcc.Graph(
                    id="choropleth-map",
                    figure=fig_map,
                    style={"height":"100vh","margin-right":"10px"}
                )
            )
        ]),
    ])
])

# === Callbacks ===

@app.callback(
    [
        Output("casos-recuperados-text","children"),
        Output("em-acompanhamento-text","children"),
        Output("casos-confirmados-text","children"),
        Output("novos-casos-text","children"),
        Output("obitos-text","children"),
        Output("obitos-na-data-text","children")
    ],
    [Input("date-picker","date"), Input("location-button","children")]
)
def display_status(date, location):
    dt = pd.to_datetime(date)
    df_sel = (
        df_brasil[df_brasil["data"]==dt]
        if location=="BRASIL"
        else df_states[(df_states["estado"]==location)&(df_states["data"]==dt)]
    )
    fmt = lambda col: "-" if pd.isna(df_sel[col].iloc[0]) else f"{int(df_sel[col].iloc[0]):,}".replace(",",".")
    return (
        fmt("Recuperadosnovos"),
        fmt("emAcompanhamentoNovos"),
        fmt("casosAcumulado"),
        fmt("casosNovos"),
        fmt("obitosAcumulado"),
        fmt("obitosNovos")
    )

@app.callback(
    Output("date-picker","min_date_allowed"),
    Output("date-picker","max_date_allowed"),
    Output("date-picker","initial_visible_month"),
    Output("date-picker","date"),
    Input("year-dropdown","value")
)
def atualizar_datepicker_por_ano(anos_sel):
    if not anos_sel or "ALL" in anos_sel:
        df_sel = df_states["data"]
    else:
        df_sel = df_states[df_states["data"].dt.year.isin(anos_sel)]["data"]
    return df_sel.min(), df_sel.max(), df_sel.min(), df_sel.max()

@app.callback(
    Output("line-graph","figure"),
    Input("location-dropdown","value"),
    Input("location-button","children"),
    Input("year-dropdown","value")
)
def plot_line_graph(metric, location, anos_sel):
    df_loc = df_brasil if location=="BRASIL" else df_states[df_states["estado"]==location]
    if anos_sel and "ALL" not in anos_sel:
        df_loc = df_loc[df_loc["data"].dt.year.isin(anos_sel)]

    fig = go.Figure(layout={"template":"plotly_dark"})

    if metric in ["casosNovos", "obitosNovos"]:
        fig.add_trace(go.Bar(
            x=df_loc["data"],
            y=df_loc[metric],
            marker_color="#FF4136",
            marker_line_color="white",
            marker_line_width=0.5
        ))
    else:
        fig.add_trace(go.Scatter(
            x=df_loc["data"],
            y=df_loc[metric],
            line=dict(color="#389fd6")
        ))

    fig.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        margin=dict(l=10, r=10, b=10, t=10)
    )
    return fig

@app.callback(
    Output("choropleth-map","figure"),
    Input("date-picker","date")
)
def update_map(date):
    dt = pd.to_datetime(date)
    df_sel = df_states[df_states["data"] == dt]
    fig = px.choropleth_map(
        df_sel, geojson=brazil_states, locations="estado", color="casosAcumulado",
        color_continuous_scale="Redor", opacity=0.55,
        hover_data=["casosAcumulado","casosNovos","obitosNovos"],
        zoom=4, center={"lat":-14.5,"lon":-52.0}, map_style="carto-darkmatter"
    )
    fig.update_layout(paper_bgcolor="#242424", margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    return fig

@app.callback(
    Output("location-button","children"),
    Input("choropleth-map","clickData"),
    Input("location-button","n_clicks")
)
def update_location(clickData, n_clicks):
    ctx = dash.callback_context
    if clickData and ctx.triggered and "clickData" in ctx.triggered[0]["prop_id"]:
        return clickData["points"][0]["location"]
    return "BRASIL"

@app.callback(
    [Output("compare-text","children"), Output("compare-graph","figure")],
    Input("state1-dropdown","value"),
    Input("state2-dropdown","value"),
    Input("year-dropdown","value")
)
def compare_states(s1, s2, anos_sel):
    df = df_states
    if anos_sel and "ALL" not in anos_sel:
        df = df[df["data"].dt.year.isin(anos_sel)]
    df1 = df[df["estado"] == s1]
    df2 = df[df["estado"] == s2]

    idx1 = df1["casosNovos"].idxmax()
    day1 = df1.loc[idx1, "data"]
    val1 = df1.loc[idx1, "casosNovos"]
    idx2 = df2["casosNovos"].idxmax()
    day2 = df2.loc[idx2, "data"]
    val2 = df2.loc[idx2, "casosNovos"]

    mon1 = df1.groupby(pd.Grouper(key="data", freq="M"))["casosNovos"].sum()
    mdt1 = mon1.idxmax()
    mv1 = mon1.max()
    mon2 = df2.groupby(pd.Grouper(key="data", freq="M"))["casosNovos"].sum()
    mdt2 = mon2.idxmax()
    mv2 = mon2.max()

    fmt_num = lambda x: f"{int(x):,}".replace(",",".")
    anos_txt = (
        ", ".join(map(str, anos_sel)) if anos_sel and "ALL" not in anos_sel
        else "todos os anos"
    )

    daily_children = [
        html.Span(f"Pico diário de novos casos ({anos_txt}):", style={"fontSize":"18px"}),
        html.Br(),
        html.Span([
            "- ", html.Span(s1, style={"fontWeight":"bold"}), ": ",
            day1.strftime("%d/%m/%Y"), " → ",
            html.Span(fmt_num(val1), style={"fontWeight":"bold"}), " casos"
        ], style={"display":"block"}),
        html.Span([
            "- ", html.Span(s2, style={"fontWeight":"bold"}), ": ",
            day2.strftime("%d/%m/%Y"), " → ",
            html.Span(fmt_num(val2), style={"fontWeight":"bold"}), " casos"
        ], style={"display":"block"}),
        html.Br(),
    ]

    monthly_children = [
        html.Span(f"Pico mensal de novos casos ({anos_txt}):", style={"fontSize":"18px"}),
        html.Br(),
        html.Span([
            "- ", html.Span(s1, style={"fontWeight":"bold"}), ": ",
            mdt1.strftime("%m/%Y"), " → ",
            html.Span(fmt_num(mv1), style={"fontWeight":"bold"}), " casos"
        ], style={"display":"block"}),
        html.Span([
            "- ", html.Span(s2, style={"fontWeight":"bold"}), ": ",
            mdt2.strftime("%m/%Y"), " → ",
            html.Span(fmt_num(mv2), style={"fontWeight":"bold"}), " casos"
        ], style={"display":"block"}),
        html.Br(),
    ]

    compare_children = dbc.Row([
        dbc.Col(daily_children, md=6),
        dbc.Col(monthly_children, md=6),
    ], align="start", style={"color":"#FFF"})

    fig = go.Figure(layout={"template":"plotly_dark"})
    fig.add_trace(go.Scatter(x=df1["data"], y=df1["casosNovos"], name=s1))
    fig.add_trace(go.Scatter(x=df2["data"], y=df2["casosNovos"], name=s2))
    fig.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        margin=dict(l=10, r=10, b=10, t=30),
        legend=dict(bgcolor="rgba(0,0,0,1)"),
        xaxis_title="Data",
        yaxis_title="Novos Casos"
    )

    return compare_children, fig

if __name__ == "__main__":
    app.run(debug=False, port=8051)