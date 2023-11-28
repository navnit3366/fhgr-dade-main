# Import
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

### DATEN AUFGABEN
# Dateipfad
url = "./newDataset.csv"
# Daten aus CSV-Datei laden
datafile = pd.read_csv(url)
# Daten für die ausgewählten Länder und Jahre filtern
countries = ['Switzerland', 'Germany', 'France', 'Austria', 'Italy', 'Liechtenstein']
filtComb = datafile.query('GeoAreaName in @countries')
# Daten für alle Länder
allCount = datafile['GeoAreaName'].unique()
# Diagramm für Tab 1
scatfig = px.line(filtComb, x="Year", y="Value", color='GeoAreaName')
hisfig = px.histogram(filtComb, x="Year", y="Value", color='GeoAreaName', barmode='group')

################################################################################################

### DATEN BEREINIGT
# Bereinigter Datensatz
data = pd.read_csv('./woman-leadership_bereinigt-neu.csv')
# Datensatz nach Jahr sortiert für animation_frame
data = data.sort_values(by="Year", ascending=True)

################################################################################################

### FÜR LINIENDIAGRAMM
# Datensatz nach Land sortiert
data1 = data.sort_values(by="Country Name", ascending=True)
# Daten für alle Länder
allCountry = data1['Country Name'].unique()

################################################################################################

### DEFAULT WERT SCHWEIZ IM LINIENDIAGRAMM
# Daten für Switzerland filtern
default_country = 'Switzerland'
default_data = data[data['Country Name'] == default_country]
# Liniendiagramm für Switzerland erstellen
default_fig = px.line(default_data, x="Year", y="Value", color='Country Name')

################################################################################################

### KARTE
# Plotly choropleth map
hover_data = ["Country Name", "Year", "Value"]
mapfig = px.choropleth(data_frame=data,
                       color_continuous_scale=px.colors.sequential.Purples,
                       color="Value",
                       hover_data=hover_data,
                       locations='Country Code',
                       animation_frame='Year')

mapfig.update_layout(
   margin={"r":0,"t":0,"l":0,"b":0},
    width=1500, 
    height=800,
    showlegend=False
)

################################################################################################

### FÜR RANGLISTE
rangdatasort = data[data["Year"] == 2020].sort_values(by="Value", ascending=False)
rang_data = ["Country Name", "Year", "Value"]
bafig = px.bar(rangdatasort,
               x="Value",
               y="Country Name",
               orientation="h",
               color="Country Name")
bafig.update_layout(
    title='Ranking of 2020',
    autosize=True,
    width=1000,
    height=1200
)

################################################################################################

# Web-App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = html.Div([

    # MAP auf Startseite
    html.H1("Female share of employment in senior and middle management (%)",
            style={'text-align': 'center'}),
    html.Div([
        dcc.Graph(
            id='chormap',
            figure=mapfig,
            responsive=True
        )
    ]),
    
    ################################################################################################
    dbc.Tabs([
        # TAB 2 -------------------------------------------------------------------------------------
        # Ländervergleich, Input Dropdown Mehrfach Auswahl, Output Liniendiagramm
        dbc.Tab(label='Country Comparison', children=[ 
            html.H6("Disclaimer: Some countries have missing data."),
            html.Label("Choose countries:", style={'text-align': 'center'}),
                    dcc.Dropdown(
                        id='lin1-dropdown',
                        options=[{'label': color, 'value': color} for color in allCountry],
                        value='Switzerland',
                        multi=True  # Mehrfachauswahl ermöglichen
                    ),
                    dcc.Graph(id='lin1-plot', figure=default_fig)
        ]),
        ################################################################################################
        # TAB 1 -------------------------------------------------------------------------------------
        dbc.Tab(label='Switzerland and neighbors', children=[
            html.H2("Switzerland and its neighboring countries",
                    style={'text-align': 'center'}),
            html.H4("Data for Switzerland, Austria, Germany and Italy",
                    style={'text-align': 'center'}),

            dcc.RangeSlider(
                id='scatter-slider',
                min=datafile['Year'].min(),
                max=datafile['Year'].max(),
                value=[datafile['Year'].min(), datafile['Year'].max()],
                marks={str(value): str(value) for value in datafile['Year'].unique()},
                step=None
            ),
                    dcc.Graph(id='hist-plot', figure=hisfig)
        ]), 
        ################################################################################################
        # TAB 3 -------------------------------------------------------------------------------------
         dbc.Tab(label='Ranking', children=[
            html.H1("Ranking", style={'text-align': 'center'}),
            html.Label("Choose a year:"),
            dcc.Dropdown(
                id='rank-dropdown',
                options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
                value=2020  # Standardwert auf 2020 setzen
            ),
            html.Div([
                dcc.Graph(
                    # Rangliste
                    id='bafig1',
                    figure=bafig,
                )
            ])
        ]),
    ])
])

################################################################################################

# Callbacks
@app.callback(Output('hist-plot', 'figure'), Input('scatter-slider', 'value'))
def update_histogram_plot(value):
    filtered_data = filtComb[(filtComb['Year'] >= value[0]) & (filtComb['Year'] <= value[1])]
    fig = px.histogram(filtered_data, x="Year", y="Value", color='GeoAreaName', barmode='group')
    return fig


@app.callback(Output('lin1-plot', 'figure'), Input('lin1-dropdown', 'value'), Input('scatter-slider', 'value'))
def update_lin1_plot(countries, value):
    filtered_data = data[(data['Country Name'].isin(countries)) & (data['Year'] >= value[0]) & (data['Year'] <= value[1])]
    fig = px.line(filtered_data, x="Year", y="Value", color='Country Name')
    return fig

@app.callback(Output('bafig1', 'figure'), Input('rank-dropdown', 'value'))
def update_rank_plot(value):
    filtered_data = data[data['Year'] == value].sort_values(by="Value", ascending=False)
    fig = px.bar(filtered_data,
                 x="Value",
                 y="Country Name",
                 orientation="h",
                 color="Country Name")
    fig.update_layout(
        title='Rangliste vom Jahr {value}',
        autosize=True,
        width=1000,
        height=1200
    )
    return fig

################################################################################################

if __name__ == '__main__':
    app.run_server(debug=False, port=8013)