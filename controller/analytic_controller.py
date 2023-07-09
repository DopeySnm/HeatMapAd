from db.db_helper import DBHelper
from mapService.heatMapWork import HeatMapWork
from parsers.base import Parser
# import ipywidgets as widgets
# from ipywidgets import interactive, interactive_output, HBox, VBox, Layout, interact
# from IPython.display import display


class AnalyticController:
    def check_city(self, city: str):
        if city == "Челябинск":
            return True

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

        result_ad = DBHelper().get_ads_by_city(city=city)
        temp_data = []

        for ad in result_ad:
            if min_price <= ad.price <= max_price:
                temp_data.append(ad)
        result_ad = temp_data
        temp_data.clear()

        # for ad in result_ad:
        #     if ad.description != None:
        #         if min_floor <= ad.description.floor <= max_floor:
        #             temp_data.append(ad)
        # result_ad = temp_data
        # temp_data.clear()

        # for ad in result_ad:
        #     if min_total_area <= ad.price <= max_total_area:
        #         temp_data.append(ad)
        # result_ad = temp_data
        # temp_data.clear()

        # for ad in result_ad:
        #     if resale:
        #         if ad.
        #         temp_data.append(ad)
        # result_ad = temp_data
        # temp_data.clear()

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
                         not_repair: bool):

        start_location = DBHelper().get_city_center(city=city)
        hmw = HeatMapWork(start_location)

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
        hmw.set_ad_list(list_filter_ads)

        if infrastructure_objects:
            db_infrastructure = DBHelper().get_infrastructure_by_city(city=city)
            hmw.set_infrastructure_list(db_infrastructure)



        # return "Вывод:", \
        #     "Город", city, \
        #     "Минимальная цена", min_price, \
        #     "Максимальная цена", max_price, \
        #     "Объекты инраструктуры", infrastructure_objects, \
        #     "Тип карты", type_map, \
        #     "Вторичное жильё", resale, \
        #     "Новостройка", new_building, \
        #     "Минимальный этаж", min_floor, \
        #     "Максимальный этаж", max_floor, \
        #     "Минимальная общая площадь кв/м", min_total_area, \
        #     "Максимальная общая площадь кв/м", max_total_area, \
        #     "C Ремонтм", repair, \
        #     "Без ремонта", not_repair

    def show_map_in_browser(self, city: str):
        ads = DBHelper().get_ads_by_city(city)
        infrastructure = DBHelper().get_infrastructure_by_city(city)
        start_location = Parser().get_coordinates(city)

        hmw = HeatMapWork(start_location=start_location, list_ad=ads, list_infrastructure=infrastructure)
        hmw.show_map_in_browser()


if __name__ == "__main__":
    AnalyticController().start_map()