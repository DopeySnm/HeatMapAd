from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from db.base import Base

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    coordinate_x = Column(Float)
    coordinate_y = Column(Float)
    city = Column(String)
    district = Column(String)
    street = Column(String)
    house = Column(String)
    flat = Column(String)
    ad = relationship('Ad')
    infrastructure = relationship('Infrastructure')

    def __init__(self,
                coordinate_x: float,
                coordinate_y: float,
                city: str,
                district: str = None,
                street: str = None,
                house: str = None,
                flat: str = None):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.city = city
        self.district = district
        self.street = street
        self.house = house
        self.flat = flat
