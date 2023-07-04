from datetime import date
from models.location import Location

class RealEstate:
    def __init__(self,
                title: str,
                location: Location,
                date_download: date):
        self.title = title
        self.location = location
        self.date_download = date_download
