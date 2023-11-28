import pandas as pd
import plotly.express as px

# Bereinigter Datensatz
data = pd.read_csv('woman-leadership_bereinigt-neu.csv')

# Ländergrenzen als GeoJSON-Datei
with open('countries.geo.json', 'r') as f:
    geojson = f.read()

# Plotly choropleth map
fig = px.choropleth(data_frame=data,
                    geojson=geojson,
                    locations='Country Name',  # Spalte Land im CSV-file mit den Ländern
                    featureidkey='properties.name',  # Feature Ländername im GeoJson-file
                    color='Value',  # Daten aus dem CSV-file welche farblich visualisiert werden sollen
                    color_continuous_scale='YlOrRd',  # Farben Gelb-zu-Rot
                    range_color=(0, 100),  # Farbspektrum für die Visualisierung
                    scope='world',  # Map-Scope (folgende könnten auch gewählt werden: 'world', 'europe', 'asia', etc.)
                    animation_frame='Year', # Balken animiert nach Jahr // Wie umsetzen, dass die Reihenfolge stimmt?
                    labels={'Percentage': 'Women in Leadership by Country'})  # Textlabel für den Farbbalken

fig.update_layout(title='Female share of employment in senior and middle management (%)')  # Titel der Map-Visualisierung
fig.show()