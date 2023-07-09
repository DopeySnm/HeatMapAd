from db.db_helper import DBHelper
from mapService.heatMapWork import HeatMapWork
from parsers.base import Parser
# import ipywidgets as widgets
# from ipywidgets import interactive, interactive_output, HBox, VBox, Layout, interact
# from IPython.display import display


class AnalyticController:
    def get_list_city(self):
        list_city = []
        for location in DBHelper().get_list_city():
            list_city.append(location.city)
        return list_city

    def get_ads_heat_map_after_filter(self,
                            city: str,
                            min_price: int,
                            max_price: int,
                            resale: bool,
                            new_building: bool,
                            min_floor: int,
                            max_floor: int,
                            min_total_area: float,
                            max_total_area: float,
                            repair: bool,
                            not_repair: bool):

        statr_ad = DBHelper().get_ads_by_city(city=city)
        result_ad = []
        temp_data = []

        for ad in statr_ad:
            if min_price <= ad.price <= max_price:
                temp_data.append(ad)
        result_ad = temp_data.copy()
        temp_data.clear()

        for ad in result_ad:
            if ad.description.floor is None:
                if min_floor == 1 and max_floor == 10:
                    temp_data.append(ad)
            else:
                if min_floor <= ad.description.floor <= max_floor:
                    temp_data.append(ad)
        result_ad = temp_data.copy()
        temp_data.clear()

        for ad in result_ad:
            if ad.description.floor is None:
                if min_total_area == 1 and max_total_area == 10:
                    temp_data.append(ad)
            else:
                if min_total_area <= ad.description.total_area <= max_total_area:
                    temp_data.append(ad)
        result_ad = temp_data.copy()
        temp_data.clear()

        for ad in result_ad:
            if resale:
                if ad.description.housing_type == "Вторичка":
                    temp_data.append(ad)
            elif new_building:
                if ad.description.housing_type == "Новостройка" or ad.description.housing_type == "Новостройка Апартаменты":
                    temp_data.append(ad)
            else:
                temp_data.append(ad)
        result_ad = temp_data.copy()
        temp_data.clear()

        for ad in result_ad:
            if repair:
                if ad.description.repair == "Чистовая" or ad.description.repair == "Предчистовая":
                    temp_data.append(ad)
            elif not_repair:
                if ad.description.repair == "Без отделки":
                    temp_data.append(ad)
            else:
                temp_data.append(ad)
        result_ad = temp_data.copy()
        temp_data.clear()

        return result_ad


    def get_img_analytical_map(self,
                                city: str,
                                infrastructure_objects: bool,
                                type_map: str, ):
        return "Вывод: ", \
            "Город", city, \
            "Объекты инраструктуры", infrastructure_objects, \
            "Тип карты", type_map

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
                         max_total_area: float,
                         repair: bool,
                         not_repair: bool,
                         id_tg_user: int):

        start_location = DBHelper().get_city_center(city=city)
        list_filter_ads = self.get_ads_heat_map_after_filter(
            city=city,
            min_price=min_price,
            max_price=max_price,
            resale=resale,
            new_building=new_building,
            min_floor=min_floor,
            max_floor=max_floor,
            min_total_area=min_total_area,
            max_total_area=max_total_area,
            repair=repair,
            not_repair=not_repair)

        hmw = HeatMapWork(start_location, list_filter_ads)

        if infrastructure_objects:
            db_infrastructure = DBHelper().get_infrastructure_by_city(city=city)
            hmw.set_list_infrastructure(list_infrastructure=db_infrastructure)

        hmw.get_png(id_tg_user)

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
            "Максимальная общая площадь кв/м", max_total_area, \
            "C Ремонтм", repair, \
            "Без ремонта", not_repair

    # def show_map_in_browser(self, city: str):
    #     ads = DBHelper().get_ads_by_city(city)
    #     infrastructure = DBHelper().get_infrastructure_by_city(city)
    #     start_location = Parser().get_coordinates(city)
    #
    #     hmw = HeatMapWork(start_location=start_location, list_ad=ads, list_infrastructure=infrastructure)
    #     hmw.show_map_in_browser()

#
# if __name__ == "__main__":
#     AnalyticController().start_map()