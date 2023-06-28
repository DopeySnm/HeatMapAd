from model.description import Description
from model.location import Location

class RealEstate:
    def __init__(self,
                title: str,
                location: Location,
                description: Description):
        self.title = title
        self.location = location
        self.description = description
