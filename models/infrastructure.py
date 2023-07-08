from datetime import date

from sqlalchemy.orm import relationship

from db.base import Base
from models.location import Location
from models.real_estate import RealEstate
from sqlalchemy import Column, Integer, String, ForeignKey, Date

class Infrastructure(RealEstate, Base):
    __tablename__ = 'infrastructure'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    type = Column(String)
    date_download = Column(Date)
    location_id = Column(Integer, ForeignKey('location.id'))

    location = relationship('Location', back_populates="infrastructure")

    def __init__(self,
                 type: str,
                 title: str,
                 location: Location,
                 date_download: date):
        super().__init__(title, location, date_download)
        self.type = type