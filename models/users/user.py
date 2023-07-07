from db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    id_telegram = Column(Integer, unique=True)
    user_name = Column(String)
    is_admin = Column(Boolean)

    tokens = relationship('Tokens', back_populates="user")
    history = relationship('History', back_populates="user")
    favourites = relationship('Favourites', back_populates="user")

    def __init__(self,
                 user_name: str,
                 is_admin: bool,
                 id_telegram: int,
                 list_favourites: list = None,
                 list_history: list = None,
                 count_token: int = None):
        self.user_name = user_name
        self.is_admin = is_admin
        self.id_telegram = id_telegram
        self.list_favourites = list_favourites
        self.list_history = list_history
        self.count_token = count_token
