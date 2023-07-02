from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from db.base import Base

class Description(Base):
    __tablename__ = 'description'

    id = Column(Integer, primary_key=True)
    ad = relationship('Ad')
    def __init__(self, *args):
        self.args = [args]