from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash (_name_)

# Bereinigter Datensatz
data = pd.read_csv('woman-leadership_bereinigt-neu.csv')

# Datensatz nach Jahr sortiert für animation_frame
data = data.sort_values(by="Year", ascending=True)

# Plotly choropleth map
hover_data = ["Country Name", "Year", "Value"] # Daten, welche angezeigt werden beim Hovering auf ein Land
fig = px.choropleth(data_frame=data,
                    color_continuous_scale=px.colors.sequential.Blues, # Farbspektrum für die Visualisierung des «Value»-Balken
                    color="Value", # Darstellung «Value»-Balken
                    hover_data = hover_data, # Definition hover
                    locations='Country Code',  # Spalte mit Iso Alpha-3 Ländercodes im CSV-file
                    animation_frame='Year', # Balken animiert mit Jahr der Daten
                    ) 

fig.update_layout(title='Female share of employment in senior and middle management (%)')  # Titel der Map-Visualisierung
app.layout = html.Div([html.H1("Female share of employment in senior and middle management (%)"),
    dcc.Graph(figure=fig)
])

if _name_ == '_main_':
    app.run_server(debug=True)