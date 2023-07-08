from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String,  ForeignKey
from db.base import Base
from models.users.user import User

class Favourites(Base):
    __tablename__ = 'favourites'

    id = Column(Integer, primary_key=True)
    link_ad = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates="favourites")
    def __init__(self,
                 link_ad: str,
                 user: User):
        self.link_ad = link_ad
        self.user = user
