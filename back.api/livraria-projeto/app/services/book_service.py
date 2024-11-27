from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book_schemas import BookCreate, BookUpdate, BookResponse

class BookService:
    def __init__(self, db: Session):
        self.book_repository = BookRepository(db)
        self.db = db

    def create_book(self, book_data: BookCreate) -> BookResponse:
        # Verifica se livro com ISBN já existe
        existing_book = self.book_repository.get_by_isbn(book_data.isbn)
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )

        new_book = self.book_repository.create(book_data)
        return BookResponse.from_orm(new_book)

    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return BookResponse.from_orm(book)

    def get_books_by_title(self, title: str) -> List[BookResponse]:
        books = self.book_repository.get_by_title(title)
        return [BookResponse.from_orm(book) for book in books]

    def update_book(self, book_id: int, book_data: BookUpdate) -> BookResponse:
        existing_book = self.book_repository.get_by_id(book_id)
        if not existing_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        updated_book = self.book_repository.update(book_id, book_data)
        return BookResponse.from_orm(updated_book)

    def delete_book(self, book_id: int) -> None:
        existing_book = self.book_repository.get_by_id(book_id)
        if not existing_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        self.book_repository.delete(book_id)

    def check_book_availability(self, book_id: int) -> bool:
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return book.available_copies > 0