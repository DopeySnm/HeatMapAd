from db.db_helper import DBHelper
from mapService.heatMapWork import Render
from parsers.base import Parser
class AnalyticController:
    def get_map_html(self, city, name_path, max_price, min_price, max_total_area, min_total_area, min_floor, max_floor, housing_type):
        ads = DBHelper().get_ads_by_city(city)
        infrastructure = DBHelper().get_infrastructure_by_city(city=city)
        start_location = DBHelper().get_city_center(city=city)

        ads = self.handler_filters(ads, max_price, min_price, max_total_area, min_total_area, min_floor, max_floor, housing_type)

        hmw = Render(start_location=start_location, list_ad=ads, list_infrastructure=infrastructure)
        hmw.save_map_to_path(name_path=name_path)

    def check_numbers(self, min_number, max_number):
        if min_number < max_number:
            pass
        elif min_number > max_number:
            min_number, max_number = max_number, min_number
        elif min_number == max_number:
            pass
        return min_number, max_number

    def handler_filters(self, list_ads, max_price, min_price, max_total_area, min_total_area, min_floor, max_floor, housing_type):
        result_list_ads = []

        price_ads = []
        for ad in list_ads:
            # CHECK PRICE
            min_price, max_price = self.check_numbers(int(min_price), int(max_price))
            if ad.price is not None:
                if min_price <= ad.price <= max_price:
                    price_ads.append(ad)

        total_area_ads = []
        for ad in list_ads:
            # CHECK TOTAL AREA
            min_total_area, max_total_area = self.check_numbers(float(min_total_area), float(max_total_area))
            if ad.description.total_area is not None:
                if min_total_area <= ad.description.total_area <= max_total_area:
                    total_area_ads.append(ad)

        floor_ads = []
        for ad in list_ads:
            # CHECK FLOOR
            min_floor, max_floor = self.check_numbers(int(min_floor), int(max_floor))
            if ad.description.floor is not None:
                if min_floor <= ad.description.floor <= max_floor:
                    floor_ads.append(ad)

        housing_type_ads = []
        for ad in list_ads:
            # CHECK HOUSING TYPE
            if ad.description.housing_type is not None:
                if ad.description.housing_type == housing_type:
                    housing_type_ads.append(ad)
                elif housing_type == "Без разницы":
                    housing_type_ads.append(ad)

        result_list_ads = self.merge_checked_lists(result_list_ads, total_area_ads, floor_ads, price_ads, housing_type_ads)
        return result_list_ads

    def merge_checked_lists(self, list_res, list1, list2, list3, list4):
        list_res = list(set(list1) & set(list2) & set(list3) & set(list4))
        return list_res

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

        hmw = Render(start_location, list_filter_ads)

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

if __name__ == "__main__":
    list_ads = DBHelper().get_ads_by_city("Челябинск")
    Render().get(list_ads[0],"ffila", 3)