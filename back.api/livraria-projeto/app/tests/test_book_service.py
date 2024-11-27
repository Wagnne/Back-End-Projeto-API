import pytest
from fastapi import HTTPException

from app.services.book_service import BookService
from app.schemas.book_schemas import BookCreate, BookUpdate

def test_create_book(test_db, sample_book):
    book_service = BookService(test_db)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    assert created_book.title == sample_book['title']
    assert created_book.isbn == sample_book['isbn']
    assert created_book.total_copies == sample_book['total_copies']

def test_create_duplicate_book(test_db, sample_book):
    book_service = BookService(test_db)
    
    # Cria primeiro livro
    book_create = BookCreate(**sample_book)
    book_service.create_book(book_create)
    
    # Tenta criar livro com mesmo ISBN
    with pytest.raises(HTTPException) as exc_info:
        book_service.create_book(book_create)
    
    assert exc_info.value.status_code == 400
    assert "Book with this ISBN already exists" in str(exc_info.value.detail)

def test_get_book_by_title(test_db, sample_book):
    book_service = BookService(test_db)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    book_service.create_book(book_create)
    
    # Busca livro por título
    books = book_service.get_books_by_title(sample_book['title'])
    
    assert len(books) > 0
    assert books[0].title == sample_book['title']

def test_update_book(test_db, sample_book):
    book_service = BookService(test_db)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    # Atualiza livro
    update_data = BookUpdate(title="Updated Book Title")
    updated_book = book_service.update_book(created_book.id, update_data)
    
    assert updated_book.title == "Updated Book Title"

def test_delete_book(test_db, sample_book):
    book_service = BookService(test_db)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    # Deleta livro
    book_service.delete_book(created_book.id)
    
    # Verifica se livro não pode ser encontrado
    with pytest.raises(HTTPException) as exc_info:
        book_service.get_book_by_id(created_book.id)
    
    assert exc_info.value.status_code == 404

def test_check_book_availability(test_db, sample_book):
    book_service = BookService(test_db)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    # Verifica disponibilidade
    is_available = book_service.check_book_availability(created_book.id)
    
    assert is_available is True