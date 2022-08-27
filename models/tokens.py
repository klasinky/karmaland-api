from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func

from config.db import Base


# Make a SingleTone class Token
class Token(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(200), unique=True, index=True)
    expire = Integer()

    def __init__(self, token, expire):
        self.token = token
        self.expire = expire


