from typing import List
from fastapi import HTTPException
from schemas.book_schemas import Book, BookCreate, BookUpdate, BookSearchRequest

books_list = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "Brave New World", "author": "Aldous Huxley"},
]
book_id_counter = 3


async def create_book(book: BookCreate) -> Book:
    global book_id_counter
    book_id_counter += 1
    new_book = Book(id=book_id_counter, title=book.title, author=book.author)
    books_list.append(new_book.model_dump())
    return new_book


async def read_books() -> List[Book]:
    return [Book(**book_data) for book_data in books_list]


async def read_book(book_id: int) -> Book:
    for book_data in books_list:
        if book_data.get("id") == book_id:
            return Book(**book_data)
    raise HTTPException(status_code=404, detail="Книга не найдена")


async def update_book(book_id: int, book_update: BookCreate) -> Book:
    for i, book_data in enumerate(books_list):
        if book_data.get("id") == book_id:
            updated_book = Book(id=book_id, title=book_update.title, author=book_update.author)
            books_list[i] = updated_book.model_dump()
            return updated_book
    raise HTTPException(status_code=404, detail="Книга не найдена")


async def partial_update_book(book_id: int, book_update: BookUpdate) -> Book:
    for i, book_data in enumerate(books_list):
        if book_data.get("id") == book_id:
            current_book = Book(**book_data)
            update_data = book_update.model_dump(exclude_unset=True)
            updated_book_data = current_book.model_dump()
            updated_book_data.update(update_data)
            books_list[i] = updated_book_data
            return Book(**updated_book_data)
    raise HTTPException(status_code=404, detail="Книга не найдена")


async def delete_book(book_id: int) -> dict:
    global books_list
    initial_len = len(books_list)
    books_list = [book_data for book_data in books_list if book_data.get("id") != book_id]
    if len(books_list) < initial_len:
        return {"detail": "Книга удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")


async def search_book(search_params: BookSearchRequest) -> Book:
    if not search_params.title and not search_params.author:
        raise HTTPException(status_code=400, detail="Необходимо указать название или автора для поиска")

    for book_data in books_list:
        book = Book(**book_data)
        if (search_params.title and book.title == search_params.title) or \
                (search_params.author and book.author == search_params.author):
            return book

    raise HTTPException(status_code=404, detail="Книга не найдена")


async def get_books_uppercase() -> List[Book]:
    uppercase_books = []
    for book_data in books_list:
        uppercase_book_data = book_data.copy()
        uppercase_book_data["title"] = uppercase_book_data["title"].upper()
        uppercase_books.append(Book(**uppercase_book_data))
    return uppercase_books
