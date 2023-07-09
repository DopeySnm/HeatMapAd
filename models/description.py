from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db.base import Base

class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    main_description = Column(String)
    total_area = Column(Float)
    floor = Column(Integer)
    housing_type = Column(String)
    living_area = Column(Float)
    repair = Column(String)
    count_views = Column(Integer)

    ad = relationship('Ad', back_populates="description")
    def __init__(self,
                 main_description: str,
                 total_area: float = None,
                 floor: int = None,
                 living_area: str = None,
                 housing_type: str = None,
                 repair: str = None,
                 count_views: int = None):
        self.main_description = main_description
        self.total_area = total_area
        self.floor = floor
        self.housing_type = housing_type
        self.repair = repair
        self.count_views = count_views
        self.living_area = living_area
