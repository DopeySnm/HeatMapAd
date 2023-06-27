import pandas as pd
import folium
from folium.plugins import HeatMap

from city import City
from ad import Ad


class HeatMapWork:
    def __init__(self, city: City):
        self.city = city
        self.listAd = []

    def setAdList(self, data):
        self.listAd += data

    def getHtml(self):

        # df = pd.read_csv(self.path)

        myMap = folium.Map(location=(self.city.y, self.city.y),
                           max_bounds=True,
                           tiles="openstreetmap",
                           zoom_start=6,
                           min_zoom=3)

        # myMap = folium.Map(location=(55.17869847587624, 61.3284869196522),
        #                    max_bounds=True,
        #                    tiles="openstreetmap",
        #                    zoom_start=6,
        #                    min_zoom=3)

        for ad in self.listAd:
            folium.CircleMarker([ad.x, ad.y],
                                radius=5,
                                popup=folium.Popup(html=ad.getDiscription),#ad.data,  # инф при нажатии
                                color="transparent",
                                tooltip=ad.data,  # инф при наведении
                                fill=True,
                                fill_color="transparent").add_to(myMap)

        # for index, row in df.iterrows():
        #     folium.CircleMarker([row['latitude'], row['longitude']],
        #                         radius=5,
        #                         popup=row['data'],  # инф при нажатии
        #                         color="transparent",
        #                         tooltip=row['data'],  # инф при наведении
        #                         fill=True,
        #                         fill_color="transparent").add_to(myMap)

        ## matrix = df[['latitude', 'longitude', 'magnitude']]

        matrix = [[ad.x, ad.y, ad.magnitude] for ad in self.listAd]

        HeatMap(matrix).add_to(myMap)
        myMap.show_in_browser()
        return myMap.get_root().render()


objCity = City(name="Chelybinsc", x=55.17869847587624, y=61.3284869196522)

hp = HeatMapWork(city=objCity)

listAd = []
listAd.append(Ad(x=56.17869847587624, y=62.3284869196522, city=objCity, data="-квартира", magnitude=0.5))
listAd.append(Ad(x=57.17869847587624, y=63.3284869196522, city=objCity, data="квартира1", magnitude=0.5))

hp.setAdList(listAd)

map_html = hp.getHtml()