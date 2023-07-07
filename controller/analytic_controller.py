from db.db_helper import DBHelper
from mapService.heatMapWork import HeatMapWork

class AnalyticController:
    def check_city(self, city: str):
        if city == "Челябинск":
            return True

    def get_list_city(self):
        list_city = []
        for location in DBHelper().get_list_city():
            list_city.append(location.city)
        return list_city

    def get_img_heat_map(self,
                         city: str,
                         min_price: int,
                         max_price: int,
                         infrastructure_objects: bool,
                         type_map: str,
                         resale: bool,
                         new_building: bool,
                         min_floor: int,
                         max_floor: int,
                         min_total_area: float,
                         max_total_area: float):
        return "Вывод:", \
            "Город", city, \
            "Минимальная цена", min_price, \
            "Максимальная цена", max_price, \
            "Объекты инраструктуры", infrastructure_objects, \
            "Тип карты", type_map, \
            "Вторичное жильё", resale, \
            "Новостройка", new_building, \
            "Минимальный этаж", min_floor, \
            "Максимальный этаж", max_floor, \
            "Минимальная общая площадь кв/м", min_total_area, \
            "Максимальная общая площадь кв/м", max_total_area

    def show_map_in_browser(self, city: str):
        ads = DBHelper().get_ads_by_city(city)
        infrastructure = DBHelper().get_infrastructure_by_city(city)
        start_location = DBHelper().get_city_center(city)
        hmw = HeatMapWork(start_location=start_location)
        hmw.set_ad_list(ads)
        hmw.set_infrastructure_list(infrastructure)
        hmw.show_map_in_browser()