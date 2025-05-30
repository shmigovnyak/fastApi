from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union

class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str

class BookCreate(BaseModel):
    title: str
    author: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

class BookSearchRequest(BaseModel):
    title: Optional[str] = Field(None, description="Наименование книги для поиска")
    author: Optional[str] = Field(None, description="Автор книги для поиска") 