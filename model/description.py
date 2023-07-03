from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.base import Base

class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    main_description = Column(String)
    total_area = Column(Float)
    floor = Column(Integer)
    year_built = Column(Integer)
    living_area = Column(String)
    housing_type = Column(String)
    bathroom = Column(String)
    repair = Column(String)

    ad = relationship('Ad', back_populates="description")
    def __init__(self,
                 main_description: str,
                 total_area: float or None,
                 floor: int,
                 year_built: int or None,
                 living_area: str or None,
                 housing_type: str or None,
                 bathroom: str or None,
                 repair: str or None):
        self.main_description = main_description
        self.total_area = total_area
        self.floor = floor
        self.year_built = year_built
        self.living_area = living_area
        self.housing_type = housing_type
        self.bathroom = bathroom
        self.repair = repair
