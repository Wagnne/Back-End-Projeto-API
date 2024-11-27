from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.loan import LoanStatus
from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository
from app.schemas.loan_schemas import LoanCreate, LoanResponse, LoanUpdate

class LoanService:
    def __init__(self, db: Session):
        self.loan_repository = LoanRepository(db)
        self.book_repository = BookRepository(db)
        self.db = db

    def create_loan(self, loan_data: LoanCreate, user_id: int) -> LoanResponse:
        # Verificar disponibilidade do livro
        book = self.book_repository.get_by_id(loan_data.book_id)
        if not book or book.available_copies <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book not available for loan"
            )

        # Definir data de devolução (14 dias a partir da data atual)
        loan_data.loan_date = datetime.now()
        loan_data.return_date = loan_data.loan_date + timedelta(days=14)
        loan_data.user_id = user_id
        loan_data.status = LoanStatus.ACTIVE

        # Reduzir cópias disponíveis do livro
        book.available_copies -= 1
        self.book_repository.update(book.id, {"available_copies": book.available_copies})

        new_loan = self.loan_repository.create(loan_data)
        return LoanResponse.from_orm(new_loan)

    def return_book(self, loan_id: int) -> LoanResponse:
        loan = self.loan_repository.get_by_id(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )

        # Atualizar status do empréstimo
        loan.status = LoanStatus.RETURNED
        loan.actual_return_date = datetime.now()

        # Restaurar cópia disponível do livro
        book = self.book_repository.get_by_id(loan.book_id)
        book.available_copies += 1
        self.book_repository.update(book.id, {"available_copies": book.available_copies})

        updated_loan = self.loan_repository.update(loan_id, LoanUpdate(**loan.__dict__))
        return LoanResponse.from_orm(updated_loan)

    def get_user_active_loans(self, user_id: int) -> List[LoanResponse]:
        loans = self.loan_repository.get_by_user_and_status(user_id, LoanStatus.ACTIVE)
        return [LoanResponse.from_orm(loan) for loan in loans]

    def check_overdue_loans(self) -> List[LoanResponse]:
        current_date = datetime.now()
        overdue_loans = self.loan_repository.get_overdue_loans(current_date)
        return [LoanResponse.from_orm(loan) for loan in overdue_loans]