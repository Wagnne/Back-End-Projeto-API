from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.config.database import Base

class LoanStatus(enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    
    # Chaves estrangeiras
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)

    # Datas
    loan_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_return_date = Column(DateTime(timezone=True), nullable=False)
    actual_return_date = Column(DateTime(timezone=True), nullable=True)

    # Status do empréstimo
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)

    # Relacionamentos
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")

    def __repr__(self):
        return f"<Loan of {self.book.title} by {self.user.username}>"

    @property
    def is_overdue(self):
        # Verifica se o empréstimo está em atraso
        from datetime import datetime
        return (self.status == LoanStatus.ACTIVE and 
                datetime.now() > self.expected_return_date)