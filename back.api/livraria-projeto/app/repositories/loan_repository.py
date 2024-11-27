from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.loan import Loan, LoanStatus
from app.models.book import Book
from app.models.user import User
from app.schemas.loan_schemas import LoanCreate

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, loan: LoanCreate, user_id: int) -> Loan:
        """
        Cria um novo empréstimo
        """
        # Calcula data de devolução esperada (14 dias a partir da data atual)
        expected_return_date = datetime.now() + timedelta(days=14)

        db_loan = Loan(
            user_id=user_id,
            book_id=loan.book_id,
            expected_return_date=expected_return_date,
            status=LoanStatus.ACTIVE
        )
        self.db.add(db_loan)
        self.db.commit()
        self.db.refresh(db_loan)
        return db_loan

    def get_by_id(self, loan_id: int) -> Loan:
        """
        Busca um empréstimo pelo ID
        """
        return self.db.query(Loan).filter(Loan.id == loan_id).first()

    def list_user_loans(self, user_id: int, status: LoanStatus = None):
        """
        Lista empréstimos de um usuário, com opção de filtrar por status
        """
        query = self.db.query(Loan).filter(Loan.user_id == user_id)
        if status:
            query = query.filter(Loan.status == status)
        return query.all()

    def list_overdue_loans(self):
        """
        Lista todos os empréstimos em atraso
        """
        now = datetime.now()
        return (
            self.db.query(Loan)
            .filter(
                Loan.status == LoanStatus.ACTIVE,
                Loan.expected_return_date < now
            )
            .all()
        )

    def return_book(self, loan_id: int):
        """
        Registra a devolução de um livro
        """
        db_loan = self.db.query(Loan).filter(Loan.id == loan_id).first()
        if db_loan:
            db_loan.actual_return_date = datetime.now()
            db_loan.status = (
                LoanStatus.RETURNED 
                if db_loan.expected_return_date >= datetime.now() 
                else LoanStatus.OVERDUE
            )
            self.db.commit()
            self.db.refresh(db_loan)
        return db_loan

    def count_active_loans(self, user_id: int):
        """
        Conta o número de empréstimos ativos de um usuário
        """
        return (
            self.db.query(Loan)
            .filter(
                Loan.user_id == user_id, 
                Loan.status == LoanStatus.ACTIVE
            )
            .count()
        )

    def get_loan_statistics(self):
        """
        Estatísticas gerais de empréstimos
        """
        total_loans = self.db.query(Loan).count()
        active_loans = self.db.query(Loan).filter(Loan.status == LoanStatus.ACTIVE).count()
        overdue_loans = self.db.query(Loan).filter(Loan.status == LoanStatus.OVERDUE).count()

        return {
            "total_loans": total_loans,
            "active_loans": active_loans,
            "overdue_loans": overdue_loans
        }