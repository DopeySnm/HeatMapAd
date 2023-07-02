from datetime import date
from db.base import Base
from model.description import Description
from model.location import Location
from model.real_estate import RealEstate
from sqlalchemy import Column, Integer, String,  ForeignKey, Float, Date

class Ad(RealEstate, Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    linc = Column(String)
    title = Column(String)
    magnitude = Column(Float)
    data_download = Column(Date)
    location = Column(Integer, ForeignKey('location.id'))
    description = Column(Integer, ForeignKey('description.id'))

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