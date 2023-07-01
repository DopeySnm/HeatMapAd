from datetime import date
from model.location import Location
from model.real_estate import RealEstate


class Infrastructure(RealEstate):
    def __init__(self,
                 type: str,
                 title: str,
                 location: Location,
                 data_download: date):
        super().__init__(title, location, data_download)
        self.type = type