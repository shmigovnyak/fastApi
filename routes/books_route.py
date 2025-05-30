from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Union

# 1. Создать модель книги Book
class Book(BaseModel):
    id: int
    title: str
    author: str

# Исходные данные книг
books_list = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "Brave New World", "author": "Aldous Huxley"},
]

# Модель для запроса поиска книг
class BookSearchRequest(BaseModel):
    title: Optional[str] = Field(None, description="Наименование книги для поиска")
    author: Optional[str] = Field(None, description="Автор книги для поиска")

router = APIRouter(
    prefix="/v1/books",
    tags=["books"],
)

# 2. Реализовать POST метод /v1/books/search
@router.post("/search", response_model=Book)
async def search_book(search_params: BookSearchRequest):
    if not search_params.title and not search_params.author:
        raise HTTPException(status_code=400, detail="Необходимо указать название или автора для поиска")

    for book_data in books_list:
        book = Book(**book_data)
        if (search_params.title and book.title == search_params.title) or \
           (search_params.author and book.author == search_params.author):
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")

# 3. Реализовать GET метод /v1/books/uppercase
@router.get("/uppercase", response_model=List[Book])
async def get_books_uppercase():
    uppercase_books = []
    for book_data in books_list:
        uppercase_book_data = book_data.copy()
        uppercase_book_data["title"] = uppercase_book_data["title"].upper()
        uppercase_books.append(Book(**uppercase_book_data))
    return uppercase_books 