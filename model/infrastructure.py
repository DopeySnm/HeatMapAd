from datetime import date

from sqlalchemy.orm import relationship

from db.base import Base
from model.location import Location
from model.real_estate import RealEstate
from sqlalchemy import Column, Integer, String, ForeignKey, Date

class Infrastructure(RealEstate, Base):
    __tablename__ = 'infrastructure'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    data_download = Column(Date)
    location_id = Column(Integer, ForeignKey('location.id'))

    location = relationship('Location', back_populates="infrastructure")

    def __init__(self,
                 type: str,
                 title: str,
                 location: Location,
                 data_download: date):
        super().__init__(title, location, data_download)
        self.type = type