from datetime import date

from model_description import Description
from model_location import Location
from realEstate import RealEstate

class Ad(RealEstate):
    def __init__(self,
                 title: str,
                 price: float,
                 link: str,
                 location: Location,
                 magnitude: float,
                 data_download: date,
                 description: Description = None):
        super().__init__(title, location, data_download)
        self.price = price
        self.linc = link
        self.magnitude = magnitude
        self.description = description
    def __str__(self):
        return f"Заголовок: {self.title}\nЦена: {self.price}\nСсылка на объявление: {self.link}\nЛокация: {self.location}Площадь: {self.magnitude}\nДата загрузки{self.data_download}\nОписание: {self.discription}"