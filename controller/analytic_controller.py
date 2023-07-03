from db.db_helper import DBHelper
from mapService.heatMapWork import HeatMapWork

class AnalyticController:
    def show_map_in_browser(self, city: str):
        ads = DBHelper().get_ads_by_city(city)
        infrastructure = DBHelper().get_infrastructure_by_city(city)
        start_location = DBHelper().get_city_center(city)
        hmw = HeatMapWork(start_location=start_location)
        hmw.set_ad_list(ads)
        hmw.set_infrastructure_list(infrastructure)
        hmw.show_map_in_browser()

AnalyticController().show_map_in_browser("Челябинск")