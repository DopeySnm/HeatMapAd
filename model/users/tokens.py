from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from db.base import Base
class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    count_tokens = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('Users', back_populates="tokens")

    def __init__(self,
                 count_tokens: int):
        self.count_tokens = count_tokens
