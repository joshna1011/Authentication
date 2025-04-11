from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    image_url = Column(String, nullable=True)