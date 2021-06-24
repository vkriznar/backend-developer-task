from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    username = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(64), nullable=False)
    salt = Column(String(32), nullable=False)
