import pandas as pd
import folium
from folium.plugins import HeatMap

df = pd.read_csv('./data.txt')

myMap = folium.Map(location=(55.17869847587624, 61.3284869196522),
                   max_bounds=True,
                   tiles="openstreetmap",
                   zoom_start=5,
                   min_zoom=1)

for index, row in df.iterrows():
    folium.CircleMarker([row['latitude'], row['longitude']],
                        radius=5,
                        popup=row['data'],
                        color="transparent",
                        fill=True,
                        fill_color="transparent").add_to(myMap)


matrix = df[['latitude', 'longitude', 'magnitude']]

HeatMap(matrix).add_to(myMap)

myMap.show_in_browser()