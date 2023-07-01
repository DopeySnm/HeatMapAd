from model.location import Location
from datetime import date

class RealEstate:
    def __init__(self,
                title: str,
                location: Location,
                data_download: date):
        self.title = title
        self.location = location
        self.data_download = data_download