from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

import loaddata as ld

app = Dash(__name__)

data = ld.load_data()

data_worksyear = data["year"].value_counts().sort_index()

fig_worksyear = px.line(
    x = data_worksyear.index,
    y = data_worksyear.values,
    labels = {
        "x": "Année",
        "y": "Oeuvres reçues"
    },
    title= "Oeuvres reçues par an",
    markers=True
)

dlyears = pd.DatetimeIndex(data["date_reception"]).year.unique().dropna().sort_values()

app.layout = html.Div([
    html.H1("Dépôt légal à la Cinémathèque québécoise"),
    dcc.Graph(figure=fig_worksyear),
    dcc.Graph(id="typele_year"),
    dcc.Checklist(
        options = ld.typele_uniqes(data),
        value=[ld.typele_uniqes(data)[-1]],
        id="types_element"
    ),
    dcc.Graph(id="prods_annee"),
    dcc.Dropdown(
        dlyears,
        id="annee_drop"
    ),
    html.Div(children=[
        dcc.Graph(id="recep_socprod", style={'display': 'inline-block'}),
        dcc.Graph(id="socprod_typeles", style={'display': 'inline-block'})
    ]),
    dcc.Dropdown(
        ld.unique_socprods(data),
        id="socprod_ddown",
        value=ld.unique_socprods(data)[0]
    )    
])


@app.callback(
    Output("typele_year", "figure"), 
    Input("types_element", "value"))
def update_line_chart(typeles):
    df = ld.typele_peryear(data)
    mask = df.types_element.isin(typeles)
    fig = px.line(
        df[mask], 
        x="year", y="size", color='types_element',
        title="Types d'élément reçus par an",
        labels={
            "year" : "Année",
            "size" : "Oeuvres déposées",
            "types_element": "Type d'élément"
        },
        markers=True
    )
    return fig


@app.callback(
    Output('prods_annee', 'figure'),
    Input('annee_drop', 'value'))
def update_graph(selected_year):
    filtered_df = data
    if isinstance(selected_year, int):
        filtered_df = filtered_df[pd.DatetimeIndex(data["date_reception"]).year == selected_year]

    filtered_df = filtered_df["societe_production"].dropna()

    filtered_df = filtered_df.apply(lambda x : x.split(";")).explode()

    filtered_df = filtered_df.value_counts().head(10)

    fig = px.bar(
        title= "Top 10 sociétés de production",
        x=filtered_df.index, 
        y=filtered_df.values,
        labels={
            "x" : "Société de production",
            "y" : "Oeuvres déposées" 
        }
    )

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('recep_socprod', 'figure'),
    Input("socprod_ddown", 'value'))
def update_graph(socprod):
    df = ld.socprods_explode(data)
    df = df.groupby(["societe_production", "year"], as_index=False).size()
    mask = df["societe_production"] == socprod

    fig = px.line(
        df[mask],
        title = "Oeuvres déposées par an",
        x="year", y="size",
        labels={
            "year" : "Année",
            "size" : "Oeuvres déposées"
        },
        markers=True
    )

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('socprod_typeles', 'figure'),
    Input("socprod_ddown", 'value'))
def update_graph(socprod):
    df = ld.socprods_explode(data)
    df = df.groupby(["societe_production", "types_element"], as_index=False).size()
    mask = df["societe_production"] == socprod

    fig = px.bar(
        df[mask],
        title = "Types d'éléments déposés",
        x="types_element", y="size",
        labels={
            "types_element" : "Type d'élément",
            "size" : "Oeuvres déposées"
        },
        text_auto=True
    )

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)