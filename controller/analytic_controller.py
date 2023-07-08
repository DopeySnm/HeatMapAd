from db.db_helper import DBHelper
from mapService.heatMapWork import HeatMapWork
from parsers.base import Parser
import ipywidgets as widgets
from ipywidgets import interactive, interactive_output, HBox, VBox, Layout, interact
from IPython.display import display


class AnalyticController:
    def get_map(self, city: str, price, housing_type, repair, total_area, floor):
        ads = DBHelper().get_ads_by_city(city)
        infrastructure = DBHelper().get_infrastructure_by_city(city)
        start_location = Parser().get_coordinates(city)

        hmw = HeatMapWork(start_location=start_location, list_ad=ads, list_infrastructure=infrastructure)
        hmw.show_map_in_browser()


if __name__ == "__main__":
    AnalyticController().start_map()