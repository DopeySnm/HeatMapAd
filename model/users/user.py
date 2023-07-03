from db.base import Base
from model.users.favourites import Favourites
from model.users.history import History
from model.users.tokens import Tokens
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    #tokens_id = Column(Integer, ForeignKey('tokens.id'))

    tokens = relationship('Tokens', back_populates="users")
    history = relationship('History', back_populates="users")
    favourites = relationship('Favourites', back_populates="users")

    def __init__(self,
                 user_name: str,
                 tokens: Tokens,
                 favourites: Favourites,
                 history: History):
        self.user_name = user_name
        self.tokens = tokens
        self.favourites = favourites
        self.history = history
