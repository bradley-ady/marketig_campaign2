
# dashboard.py — Marketing Analytics Dashboard
# Lancer avec : python dashboard.py
# Accéder sur : http://127.0.0.1:8050

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

# ── Chargement des données enrichies ────────────────────────────────────────
df = pd.read_csv("marketing_clean_segmented.csv", sep=";", encoding="utf-8-sig")

PALETTE = ["#e94560", "#0f3460", "#533483", "#05c46b"]
SEGMENTS = sorted(df["SegmentLabel"].unique().tolist())

# ── App ──────────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Marketing BI Dashboard"

# ── Layout ───────────────────────────────────────────────────────────────────
app.layout = dbc.Container([

    # Header
    dbc.Row([
        dbc.Col([
            html.H1("📊 Marketing Analytics Dashboard",
                    className="text-center my-3",
                    style={"color": "#e94560", "fontWeight": "bold"}),
            html.P("Business Intelligence & Decision Intelligence — Bachelor 3 YNOV",
                   className="text-center text-muted mb-4")
        ])
    ]),

    # KPI Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"{len(df):,}", className="card-title text-center", style={"color":"#05c46b","fontSize":"2em"}),
                html.P("Clients analysés", className="card-text text-center text-muted")
            ])
        ], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"{df['Response'].mean()*100:.1f}%", className="card-title text-center", style={"color":"#e94560","fontSize":"2em"}),
                html.P("Taux de réponse global", className="card-text text-center text-muted")
            ])
        ], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"{df['TotalSpend'].mean():.0f}€", className="card-title text-center", style={"color":"#ffa41b","fontSize":"2em"}),
                html.P("Dépense moyenne (2 ans)", className="card-text text-center text-muted")
            ])
        ], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(f"{df['ScoreCampagne_100'].mean():.1f}/100", className="card-title text-center", style={"color":"#0f3460","fontSize":"2em"}),
                html.P("Score moyen campagne", className="card-text text-center text-muted")
            ])
        ], color="dark", outline=True), width=3),
    ], className="mb-4"),

    # Tabs
    dbc.Tabs([

        # Tab 1 — Portefeuille
        dbc.Tab(label="🏠 Portefeuille", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="hist_income"), width=6),
                dbc.Col(dcc.Graph(id="pie_education"), width=6),
            ], className="mt-3"),
            dbc.Row([
                dbc.Col(dcc.Graph(id="scatter_income_spend"), width=12)
            ])
        ]),

        # Tab 2 — Segmentation
        dbc.Tab(label="🧩 Segmentation", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Axe X :", className="text-light mt-3"),
                    dcc.Dropdown(id="seg_x",
                                 options=[{"label": c, "value": c} for c in
                                          ["Income","TotalSpend","Age","Recency","ScoreCampagne_100","RFM_score"]],
                                 value="Income", clearable=False,
                                 style={"color":"#000"}),
                    html.Label("Axe Y :", className="text-light mt-2"),
                    dcc.Dropdown(id="seg_y",
                                 options=[{"label": c, "value": c} for c in
                                          ["TotalSpend","Income","Age","Recency","ScoreCampagne_100","RFM_score"]],
                                 value="TotalSpend", clearable=False,
                                 style={"color":"#000"}),
                ], width=3),
                dbc.Col(dcc.Graph(id="seg_scatter"), width=9)
            ], className="mt-3"),
            dbc.Row([dbc.Col(dcc.Graph(id="seg_bar_kpi"), width=12)])
        ]),

        # Tab 3 — Campagnes
        dbc.Tab(label="📣 Campagnes", children=[
            dbc.Row([
                dbc.Col(dcc.Graph(id="cmp_rates"), width=6),
                dbc.Col(dcc.Graph(id="cmp_by_segment"), width=6),
            ], className="mt-3"),
            dbc.Row([dbc.Col(dcc.Graph(id="score_distribution"), width=12)])
        ]),

        # Tab 4 — KPI Exécutifs
        dbc.Tab(label="📋 KPI Exécutifs", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Filtrer par segment :", className="text-light mt-3"),
                    dcc.Dropdown(id="kpi_segment",
                                 options=[{"label": "Tous", "value": "Tous"}] +
                                         [{"label": s, "value": s} for s in SEGMENTS],
                                 value="Tous", clearable=False,
                                 style={"color":"#000"}),
                ], width=4)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="kpi_rfm"), width=6),
                dbc.Col(dcc.Graph(id="kpi_channels"), width=6),
            ], className="mt-2"),
            dbc.Row([dbc.Col(html.Div(id="kpi_table"), width=12)])
        ]),

    ])

], fluid=True)


# ── Callbacks ─────────────────────────────────────────────────────────────────

@app.callback(
    Output("hist_income","figure"),
    Output("pie_education","figure"),
    Output("scatter_income_spend","figure"),
    Input("hist_income","id")
)
def tab_portfolio(_):
    fig1 = px.histogram(df, x="Income", color="SegmentLabel", nbins=50,
                        title="Distribution du Revenu par Segment",
                        color_discrete_sequence=PALETTE, template="plotly_dark")
    fig2 = px.pie(df, names="Education", title="Répartition par Niveau d'Éducation",
                  color_discrete_sequence=PALETTE, template="plotly_dark", hole=0.4)
    fig3 = px.scatter(df, x="Income", y="TotalSpend", color="SegmentLabel",
                      size="ScoreCampagne_100", size_max=15, opacity=0.6,
                      title="Income vs Dépenses — taille = Score Campagne",
                      color_discrete_sequence=PALETTE, template="plotly_dark",
                      hover_data=["Age","Education","RFM_score"])
    return fig1, fig2, fig3


@app.callback(
    Output("seg_scatter","figure"),
    Output("seg_bar_kpi","figure"),
    Input("seg_x","value"),
    Input("seg_y","value")
)
def tab_segmentation(x, y):
    fig1 = px.scatter(df, x=x, y=y, color="SegmentLabel",
                      title=f"Segmentation — {x} vs {y}",
                      color_discrete_sequence=PALETTE, template="plotly_dark",
                      opacity=0.5, hover_data=["Education","Age","Response"])

    seg_kpi = df.groupby("SegmentLabel").agg(
        Income=("Income","mean"),
        Depenses=("TotalSpend","mean"),
        Reponse=("Response",lambda x: x.mean()*100),
        RFM=("RFM_score","mean")
    ).reset_index()

    fig2 = go.Figure()
    for col, label in [("Income","Revenu moy"),("Depenses","Dépenses moy"),("Reponse","Taux réponse %"),("RFM","Score RFM")]:
        fig2.add_trace(go.Bar(name=label, x=seg_kpi["SegmentLabel"], y=seg_kpi[col]))
    fig2.update_layout(barmode="group", template="plotly_dark", title="KPI comparatif par Segment")
    return fig1, fig2


@app.callback(
    Output("cmp_rates","figure"),
    Output("cmp_by_segment","figure"),
    Output("score_distribution","figure"),
    Input("cmp_rates","id")
)
def tab_campaigns(_):
    cmp_cols = ["AcceptedCmp1","AcceptedCmp2","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","Response"]
    cmp_names = ["Cmp 1","Cmp 2","Cmp 3","Cmp 4","Cmp 5","Cmp 6 (cible)"]
    rates = [df[c].mean()*100 for c in cmp_cols]
    fig1 = px.bar(x=cmp_names, y=rates, color=cmp_names,
                  title="Taux d'Acceptation par Campagne (%)",
                  color_discrete_sequence=PALETTE*2, template="plotly_dark",
                  labels={"x":"Campagne","y":"Taux (%)"})

    seg_cmp = df.groupby("SegmentLabel")[cmp_cols].mean().reset_index()
    seg_cmp_melt = seg_cmp.melt(id_vars="SegmentLabel", value_vars=cmp_cols,
                                 var_name="Campagne", value_name="Taux")
    fig2 = px.bar(seg_cmp_melt, x="SegmentLabel", y="Taux", color="Campagne",
                  title="Taux d'Acceptation par Segment et Campagne",
                  barmode="group", template="plotly_dark")

    fig3 = px.histogram(df, x="ScoreCampagne_100", color="SegmentLabel",
                        nbins=40, title="Distribution du Score Campagne par Segment",
                        color_discrete_sequence=PALETTE, template="plotly_dark",
                        labels={"ScoreCampagne_100":"Score campagne (0-100)"})
    fig3.add_vline(x=40, line_dash="dash", line_color="white",
                   annotation_text="Seuil ciblage (40)", annotation_position="top right")
    return fig1, fig2, fig3


@app.callback(
    Output("kpi_rfm","figure"),
    Output("kpi_channels","figure"),
    Output("kpi_table","children"),
    Input("kpi_segment","value")
)
def tab_kpi(segment):
    dff = df if segment == "Tous" else df[df["SegmentLabel"] == segment]

    # RFM distribution
    fig1 = px.box(dff, x="SegmentLabel", y="RFM_score", color="SegmentLabel",
                  title="Distribution du Score RFM par Segment",
                  color_discrete_sequence=PALETTE, template="plotly_dark")

    # Canaux d'achat
    channels = {"Web":dff["NumWebPurchases"].mean(), "Catalogue":dff["NumCatalogPurchases"].mean(),
                "Magasin":dff["NumStorePurchases"].mean(), "Promos":dff["NumDealsPurchases"].mean()}
    fig2 = px.pie(values=list(channels.values()), names=list(channels.keys()),
                  title="Répartition des Achats par Canal",
                  color_discrete_sequence=PALETTE, template="plotly_dark", hole=0.35)

    # Table KPI
    kpi_df = pd.DataFrame({
        "KPI": ["Nb clients","Taux réponse (%)","Revenu moyen (€)","Dépense moy. (€)",
                "Score RFM moyen","Score campagne moyen","Recency moy. (j)"],
        "Valeur": [
            len(dff),
            f"{dff['Response'].mean()*100:.1f}%",
            f"{dff['Income'].mean():,.0f}",
            f"{dff['TotalSpend'].mean():,.0f}",
            f"{dff['RFM_score'].mean():.1f}/100",
            f"{dff['ScoreCampagne_100'].mean():.1f}/100",
            f"{dff['Recency'].mean():.0f}",
        ]
    })
    table = dash_table.DataTable(
        data=kpi_df.to_dict("records"),
        columns=[{"name": c, "id": c} for c in kpi_df.columns],
        style_table={"width":"50%","margin":"auto","marginTop":"20px"},
        style_header={"backgroundColor":"#0f3460","color":"white","fontWeight":"bold"},
        style_data={"backgroundColor":"#1a1a2e","color":"white"},
        style_cell={"textAlign":"center","padding":"10px"},
    )
    return fig1, fig2, table


if __name__ == "__main__":
    app.run(debug=True)
