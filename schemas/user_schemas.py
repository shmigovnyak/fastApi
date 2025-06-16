from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional


class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    is_active: bool = True

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr