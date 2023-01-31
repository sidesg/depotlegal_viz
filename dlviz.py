from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

import loaddata as ld

app = Dash(__name__)

data = ld.dqdata

dlyears = pd.DatetimeIndex(data["date_reception"]).year.unique().dropna().sort_values()
typeles = sorted(d for d in data[data["date_reception"].notna()]["types_element"].unique())

data["year"] = pd.DatetimeIndex(data["date_reception"]).year
worksperyear = data["year"].value_counts().sort_index()

worksyear = px.line(
    x = worksperyear.index,
    y = worksperyear.values
)


app.layout = html.Div([
    html.H1("Dépôt légal à la Cinémathèque québécoise"),
    dcc.Graph(figure=worksyear),
    dcc.Checklist(
        options = typeles,
        value=[typeles[-1]],
        id="types_element"
    ),
    dcc.Graph(id="typele_year"),
    dcc.Graph(id="prods_annee"),
    dcc.Dropdown(
        dlyears,
        "Année de réception",
        id="annee_drop"
    )    
])


@app.callback(
    Output("typele_year", "figure"), 
    Input("types_element", "value"))
def update_line_chart(typeles):
    df = ld.typele_peryear(data)
    mask = df.types_element.isin(typeles)
    fig = px.line(df[mask], 
        x="year", y="size", color='types_element')
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
        x=filtered_df.index, 
        y=filtered_df.values,
        labels={
            "x" : "Société de production",
            "y" : "Oeuvres déposées"
        }
    )

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)