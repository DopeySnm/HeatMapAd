import os
import time
import folium
from folium.plugins import HeatMap
from selenium import webdriver
from models.ad import Ad
from models.infrastructure import Infrastructure
from models.location import Location
from models.real_estate import RealEstate
from datetime import date

class HeatMapWork:
    def __init__(self, start_location: Location, list_ad: list, list_infrastructure: list = None):
        self.start_location = start_location
        self.list_ad = list_ad
        self.list_infrastructure = list_infrastructure

    def set_list_infrastructure(self, list_infrastructure: list):
        self.list_infrastructure = list_infrastructure

    def get_html_description(self, re: RealEstate):
        if isinstance(re, Ad):
            result_description = "Объявление: " + re.title + "<br>" + "Цена: " + re.price.__str__() + "<br>" + "Ссылка: " + re.link

        if isinstance(re, Infrastructure):
            result_description = "Тип: " + re.type + "<br>" + "Название: " + re.title

        return result_description

    def add_heat_map_ad_to_map(self):
        matrix = [[ad.location.coordinate_x, ad.location.coordinate_y, 0.5] for ad in self.list_ad]
        # создаём матрицу с кориднатами и магнитудой для тепловой карты

        HeatMap(data=matrix).add_to(self.ad_group.add_to(self.my_map))  # добавляем тепловые метки

    def add_ad_to_map(self):
        for ad in self.list_ad:  # добавляем метки с описанием
            self.ad_group.add_child(  # добавляем их в группу тепловой карты с названием "Объявления"
                folium.CircleMarker([ad.location.coordinate_x, ad.location.coordinate_y],
                                    radius=5,
                                    popup=folium.Popup(html=self.get_html_description(ad)),  # инф при нажатии
                                    color="transparent",
                                    tooltip=folium.Tooltip(text=self.get_html_description(ad)),  # инф при наведении
                                    fill=True,
                                    fill_color="transparent").add_to(self.my_map))

    def add_infrastructure_to_map(self):
        if self.list_infrastructure is not None:
            infrastructure_group = folium.FeatureGroup(name="Инфраструктуры").add_to(self.my_map)

            for infrastructure in self.list_infrastructure:  # добавляем метки с описанием
                infrastructure_group.add_child(  # добавляем их в группу тепловой карты с названием "Объявления"
                    folium.Marker([infrastructure.location.coordinate_x, infrastructure.location.coordinate_y],
                                  radius=5,
                                  popup=folium.Popup(html=self.get_html_description(infrastructure)),  # инф при нажатии
                                  tooltip=folium.Tooltip(text=self.get_html_description(infrastructure)),  # инф при наведении
                                  ).add_to(self.my_map))

    def get_png(self, id_tg_user: int):
        self.get_html_map()
        mapFname = str(id_tg_user) + '.html'
        self.my_map.save(mapFname)
        tmpurl = 'file://{path}/{mapfile}'.format(path=os.getcwd(), mapfile=mapFname)

        browser = webdriver.Chrome()
        browser.get(tmpurl)
        browser.fullscreen_window()
        time.sleep(5)
        browser.save_screenshot(str(id_tg_user) + '.png')
        browser.quit()

    def show_map_in_browser(self, name_path):
        self.get_html_map()
        self.my_map.save(name_path)

    def get_html_map(self):
        self.my_map = folium.Map(location=(self.start_location.coordinate_x, self.start_location.coordinate_y),
                           max_bounds=True,
                           tiles=folium.raster_layers.TileLayer(tiles='openstreetmap', name='Тепловая крата'),
                           zoom_start=11,
                           min_zoom=3)# создаём крату

        self.ad_group = folium.FeatureGroup(name="Объявления")  # создаём группу тепловой карты "Объявления"

        self.add_heat_map_ad_to_map() # добавляем тепловые метки объявлении

        self.add_ad_to_map() # добавляем метки объявлении с описанием

        self.add_infrastructure_to_map() # добавляем метки инфраструктур

        folium.LayerControl().add_to(self.my_map) # добавляет панельку с FeatureGroup которая позволяет скрывать их

        return self.my_map.get_root().render()