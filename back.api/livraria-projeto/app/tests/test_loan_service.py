import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.services.loan_service import LoanService
from app.services.user_service import UserService
from app.services.book_service import BookService
from app.schemas.user_schemas import UserCreate
from app.schemas.book_schemas import BookCreate
from app.schemas.loan_schemas import LoanCreate
from app.models.loan import LoanStatus

def test_create_loan(test_db, sample_user, sample_book):
    user_service = UserService(test_db)
    book_service = BookService(test_db)
    loan_service = LoanService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    # Cria empréstimo
    loan_data = LoanCreate(book_id=created_book.id)
    loan = loan_service.create_loan(loan_data, created_user.id)
    
    assert loan.book_id == created_book.id
    assert loan.user_id == created_user.id
    assert loan.status == LoanStatus.ACTIVE

def test_return_book(test_db, sample_user, sample_book):
    user_service = UserService(test_db)
    book_service = BookService(test_db)
    loan_service = LoanService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    # Cria empréstimo
    loan_data = LoanCreate(book_id=created_book.id)
    loan = loan_service.create_loan(loan_data, created_user.id)
    
    # Retorna livro
    returned_loan = loan_service.return_book(loan.id)
    
    assert returned_loan.status == LoanStatus.RETURNED
    assert returned_loan.actual_return_date is not None

def test_get_user_active_loans(test_db, sample_user, sample_book):
    user_service = UserService(test_db)
    book_service = BookService(test_db)
    loan_service = LoanService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    # Cria livro
    book_create = BookCreate(**sample_book)
    created_book = book_service.create_book(book_create)
    
    # Cria empréstimo
    loan_data = LoanCreate(book_id=created_book.id)
    loan_service.create_loan(loan_data, created_user.id)
    
    # Busca empréstimos ativos
    active_loans = loan_service.get_user_active_loans(created_user.id)
    
    assert len(active_loans) > 0
    assert active_loans[0].status == LoanStatus.ACTIVE

def test_create_loan_unavailable_book(test_db, sample_user, sample_book):
    user_service = UserService(test_db)
    book_service = BookService(test_db)
    loan_service = LoanService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    # Cria livro sem cópias disponíveis
    book_create = BookCreate(**{**sample_book, 'available_copies': 0})
    created_book = book_service.create_book(book_create)
    
    # Tenta criar empréstimo
    loan_data = LoanCreate(book_id=created_book.id)
    with pytest.raises(HTTPException) as exc_info:
        loan_service.create_loan(loan_data, created_user.id)
    
    assert exc_info.value.status_code == 400
    assert "Book not available for loan" in str(exc_info.value.detail)