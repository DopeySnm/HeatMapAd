from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String,  ForeignKey
from db.base import Base
class Favourites(Base):
    __tablename__ = 'favourites'

    id = Column(Integer, primary_key=True)
    link_ad = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('Users', back_populates="favourites")
    def __init__(self,
                 link_ad: list[str]):
        self.link_ad = link_ad
