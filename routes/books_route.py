from fastapi import APIRouter
from typing import List
from schemas.book_schemas import Book, BookCreate, BookUpdate, BookSearchRequest
from service import book_service

router = APIRouter(
    prefix="/v1/books",
    tags=["books"],
)

# CRUD методы для книг

@router.post("/", response_model=Book)
async def create_book_route(book: BookCreate):
    return await book_service.create_book(book)

@router.get("/", response_model=List[Book])
async def read_books_route():
    return await book_service.read_books()

@router.get("/uppercase", response_model=List[Book])
async def get_books_uppercase_route():
    return await book_service.get_books_uppercase()

@router.get("/{book_id}", response_model=Book)
async def read_book_route(book_id: int):
    return await book_service.read_book(book_id)

@router.put("/{book_id}", response_model=Book)
async def update_book_route(book_id: int, book_update: BookCreate):
    return await book_service.update_book(book_id, book_update)

@router.patch("/{book_id}", response_model=Book)
async def partial_update_book_route(book_id: int, book_update: BookUpdate):
    return await book_service.partial_update_book(book_id, book_update)

@router.delete("/{book_id}", response_model=dict)
async def delete_book_route(book_id: int):
    return await book_service.delete_book(book_id)
@router.post("/search", response_model=Book)
async def search_book_route(search_params: BookSearchRequest):
    return await book_service.search_book(search_params)
