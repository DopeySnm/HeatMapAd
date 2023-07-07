from datetime import date
from db.base import Base
from models.description import Description
from models.location import Location
from sqlalchemy.orm import relationship
from models.real_estate import RealEstate
from sqlalchemy import Column, Integer, String,  ForeignKey, Float, Date

class Ad(RealEstate, Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    link = Column(String)
    title = Column(String)
    magnitude = Column(Float)
    data_download = Column(Date)
    location_id = Column(Integer, ForeignKey('location.id'))
    description_id = Column(Integer, ForeignKey('description.id'))

    location = relationship('Location', back_populates="ad")
    description = relationship('Description', back_populates="ad")

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
        self.link = link
        self.magnitude = magnitude
        self.description = description
    def __str__(self):
        return f"Заголовок: {self.title}\nЦена: {self.price}\nСсылка на объявление: {self.link}\nЛокация: {self.location}Площадь: {self.magnitude}\nДата загрузки{self.data_download}\nОписание: {self.discription}"
