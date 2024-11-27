from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.book import Book
from app.schemas.book_schemas import BookCreate, BookUpdate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book: BookCreate) -> Book:
        """
        Cria um novo livro no banco de dados
        """
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_by_id(self, book_id: int) -> Book:
        """
        Busca um livro pelo ID
        """
        return self.db.query(Book).filter(Book.id == book_id).first()
