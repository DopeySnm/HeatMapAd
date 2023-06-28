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
                 description: Description = None):
        super().__init__(title, location, description)
        self.price = price
        self.linc = linc
        self.magnitude = magnitude
