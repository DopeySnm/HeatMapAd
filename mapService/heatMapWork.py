import folium
from folium.plugins import HeatMap
from model.ad import Ad
from model.infrastructure import Infrastructure
from model.location import Location
from model.real_estate import RealEstate
from datetime import date, datetime


class HeatMapWork:
    def __init__(self, start_location: Location):
        self.start_location = start_location
        self.list_ad = []
        self.list_infrastructure = []

    def set_ad_list(self, data):
        self.list_ad += data

    def set_infrastructure_list(self, data):
        self.list_infrastructure += data

    def get_html_description(self, re: RealEstate):
        if isinstance(re, Ad):
            result_description = "Объявление: " + re.title + "<br>" + "Цена: " + re.price.__str__() + "<br>" + "Ссылка: " + re.link
            if re.description != None:
                for description in re.description.args:
                    result_description.join(description.__str__())

        if isinstance(re, Infrastructure):
            result_description = "Тип: " + re.type + "<br>" + "Название: " + re.title

        return result_description

    def add_heat_map_ad_to_map(self):
        matrix = [[ad.location.coordinate_x, ad.location.coordinate_y, ad.magnitude] for ad in self.list_ad]
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
        infrastructure_group = folium.FeatureGroup(name="Инфраструктуры").add_to(self.my_map)

        for infrastructure in self.list_infrastructure:  # добавляем метки с описанием
            infrastructure_group.add_child(  # добавляем их в группу тепловой карты с названием "Объявления"
                folium.Marker([infrastructure.location.coordinate_x, infrastructure.location.coordinate_y],
                              radius=5,
                              popup=folium.Popup(html=self.get_html_description(infrastructure)),  # инф при нажатии
                              tooltip=folium.Tooltip(text=self.get_html_description(infrastructure)),  # инф при наведении
                              ).add_to(self.my_map))

    def get_html_map(self):
        self.my_map = folium.Map(location=(self.start_location.coordinate_x, self.start_location.coordinate_y),
                           max_bounds=True,
                           tiles=folium.raster_layers.TileLayer(tiles='openstreetmap', name='Тепловая крата'),
                           zoom_start=12,
                           min_zoom=3)# создаём крату

        self.ad_group = folium.FeatureGroup(name="Объявления")  # создаём группу тепловой карты "Объявления"

        self.add_heat_map_ad_to_map() # добавляем тепловые метки объявлении

        self.add_ad_to_map() # добавляем метки объявлении с описанием

        self.add_infrastructure_to_map() # добавляем метки инфраструктур

        folium.LayerControl().add_to(self.my_map) # добавляет панельку с FeatureGroup которая позволяет скрывать их

        return self.my_map.get_root().render()



def test():
    start_location = Location(city="Челябинск", coordinate_x=55.17869847587624, coordinate_y=61.3284869196522)

    hp = HeatMapWork(start_location=start_location)

    list_infrastructure = []
    list_infrastructure.append(
        Infrastructure(location=Location(coordinate_x=51.17869847587624, coordinate_y=62.3284869196522, city="Челябинск"),
                       title="Садик №3",
                       type="Образовательное учереждение",
                       data_download=date.today()))

    hp.set_infrastructure_list(list_infrastructure)

    list_ad = []
    list_ad.append(
        Ad(
            location=Location(coordinate_x=56.17869847587624, coordinate_y=62.3284869196522, city="Челябинск"),
            title="квартира",
            magnitude=0.5,
            price=1000,
            linc="Сслыка",
            data_download=date.today()))

    list_ad.append(
        Ad(
            location=Location(coordinate_x=57.17869847587624, coordinate_y=63.3284869196522, city="Челябинск"),
            title="квартира1",
            magnitude=0.5,
            price=1000,
            linc="Сслыка",
            data_download=date.today()))

    hp.set_ad_list(list_ad)

    map_html = hp.get_html_map()

    hp.my_map.show_in_browser()

test()