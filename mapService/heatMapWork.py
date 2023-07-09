import os
import time
import folium
from folium.plugins import HeatMap
from selenium import webdriver
from models.ad import Ad
from models.infrastructure import Infrastructure
from models.location import Location
from models.real_estate import RealEstate
from selenium.webdriver.common.by import By

class Render:
    def __init__(self, start_location: Location = None, list_ad: list = [], list_infrastructure: list = None):
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
        matrix = [[ad.location.coordinate_x, ad.location.coordinate_y, ad.description.count_views/1000] for ad in self.list_ad]
        # создаём матрицу с кориднатами и магнитудой для тепловой карты

        HeatMap(data=matrix).add_to(self.ad_group.add_to(self.my_map))  # добавляем тепловые метки


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

    def set_ad_on_map(self, ad: Ad):
        self.ad_group.add_child(  # добавляем их в группу тепловой карты с названием "Объявления"
            folium.CircleMarker((ad.location.coordinate_x, ad.location.coordinate_y),
                                radius=5,
                                popup=folium.Popup(html=self.get_html_description(ad)),  # инф при нажатии
                                color="transparent",
                                tooltip=folium.Tooltip(text=self.get_html_description(ad)),  # инф при наведении
                                fill=True,
                                fill_color="transparent").add_to(self.my_map))

    def get_png(self, id_tg_user: int):
        self.get_html_map()
        mapFname = str(id_tg_user) + '.html'
        self.my_map.save(mapFname)
        tmpurl = f'file://{os.getcwd()}/{mapFname}'

        browser = webdriver.Chrome()
        browser.get(tmpurl)
        browser.fullscreen_window()
        time.sleep(5)
        browser.save_screenshot(str(id_tg_user) + '.png')
        browser.quit()

    def save_map_to_path(self, name_path):
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
        for ad in self.list_ad:
            self.set_ad_on_map(ad) # добавляем метки объявлении с описанием
        self.add_infrastructure_to_map() # добавляем метки инфраструктур
        folium.LayerControl().add_to(self.my_map) # добавляет панельку с FeatureGroup которая позволяет скрывать их
        return self.my_map.get_root().render()

    def get(self, ad_object: Ad, id_user, m):
        self.my_map = folium.Map(location=(ad_object.location.coordinate_x, ad_object.location.coordinate_y),
                                 max_bounds=True,
                                 tiles=folium.raster_layers.TileLayer(tiles='openstreetmap', name='Тепловая крата'),
                                 zoom_start=11,
                                 min_zoom=3)
        self.ad_group = folium.FeatureGroup(name="Объявления")
        self.list_ad = [ad_object]
        self.add_heat_map_ad_to_map()
        self.set_ad_on_map(ad_object)

        mapFname = str(id_user) + '.html'
        self.my_map.save(mapFname)
        tmpurl = f'file://{os.getcwd()}/{mapFname}'
        driver = webdriver.Chrome()
        driver.get(tmpurl)
        driver.fullscreen_window()
        for i in range(m):
            driver.find_element(By.CLASS_NAME, "leaflet-control-zoom-in").click()
        time.sleep(5)
        driver.save_screenshot(str(id_user) + '.png')
        driver.quit()