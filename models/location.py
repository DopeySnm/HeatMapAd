from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from db.base import Base

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coordinate_x = Column(Float,)
    coordinate_y = Column(Float)
    full_address = Column(String)
    city = Column(String)
    street = Column(String)
    house = Column(String)

    ad = relationship('Ad', back_populates="location")
    infrastructure = relationship('Infrastructure', back_populates="location")

    def __init__(self,
                coordinate_x: float,
                coordinate_y: float,
                full_address: str,
                city: str,
                street: str = None,
                house: str = None):
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.full_address = full_address
        self.city = city
        self.street = street
        self.house = house

    def __str__(self):
        return f"Улица: {self.street}\nДом: {self.house}\nРайон: {self.district}"
