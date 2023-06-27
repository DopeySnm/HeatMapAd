import pandas as pd
import folium
from folium.plugins import HeatMap

class HeatMapWork:
    def __init__(self, path):
        self.path = path

    def getHtml(self):

        df = pd.read_csv(self.path)

        myMap = folium.Map(location=(55.17869847587624, 61.3284869196522),
                           max_bounds=True,
                           tiles="openstreetmap",
                           zoom_start=6,
                           min_zoom=3)

        for index, row in df.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']],
                                radius=5,
                                popup=row['data'],  # инф при нажатии
                                color="transparent",
                                tooltip=row['data'],  # инф при наведении
                                fill=True,
                                fill_color="transparent").add_to(myMap)

        matrix = df[['latitude', 'longitude', 'magnitude']]

        HeatMap(matrix).add_to(myMap)
        myMap.show_in_browser()
        return myMap.get_root().render()



hp = HeatMapWork('./data.txt')

map_html = hp.getHtml()