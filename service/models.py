from sqlalchemy import Column, Integer, String, Boolean
from service.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=True) 