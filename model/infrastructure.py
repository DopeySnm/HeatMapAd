from model.description import Description
from model.location import Location
from model.real_estate import RealEstate


class Infrastructure(RealEstate):
    def __init__(self,
                 type: str,
                 title: str,
                 location: Location,
                 description: Description = None):
        super().__init__(title, location, description)
        self.type = type