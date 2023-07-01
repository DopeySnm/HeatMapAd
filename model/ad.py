from datetime import date
from model.description import Description
from model.location import Location
from model.real_estate import RealEstate

class Ad(RealEstate):
    def __init__(self,
                 price: float,
                 linc: str,
                 title: str,
                 location: Location,
                 magnitude: float,
                 data_download: date,
                 description: Description = None):
        super().__init__(title, location, data_download)
        self.price = price
        self.linc = linc
        self.magnitude = magnitude
        self.description = description