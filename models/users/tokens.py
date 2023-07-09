from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from db.base import Base
from models.users.user import User


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    count_tokens = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates="tokens")
    def __init__(self,
                 count_tokens: int,
                 user: User):
        self.count_tokens = count_tokens
        self.user = user
