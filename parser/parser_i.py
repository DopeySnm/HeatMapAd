from models.ad import Ad
from models.description import Description
from models.location import Location


class Interface:
    def select_info_about_apartment(self, html_page) -> Ad:
        return Ad()

    def select_info_discription(self, html_page) -> Description:
        return Description()

    def select_title(self):
        pass

    def select_price(self):
        pass


    def select_link(self):
        pass

    def select_magnitude(self):
        pass

    def select_description_main(self):
        pass

    def select_data_download(self):
        pass

    def select_info_about_location(self, html_page) -> Location:
        return Location()

    def select_values(self):
         return None
