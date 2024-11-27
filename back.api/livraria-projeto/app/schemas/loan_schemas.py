from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.models.loan import LoanStatus

class LoanBase(BaseModel):
    book_id: int = Field(
        ..., 
        gt=0, 
        description="ID do livro emprestado"
    )

class LoanCreate(LoanBase):
    @validator('book_id')
    def validate_book_id(cls, v):
        # Aqui você poderia adicionar validações adicionais
        # Por exemplo, verificar se o livro existe ou está disponível
        return v

class LoanResponse(LoanBase):
    id: int
    user_id: int
    loan_date: datetime
    expected_return_date: datetime
    actual_return_date: Optional[datetime]
    status: LoanStatus

    class Config:
        orm_mode = True
        from_attributes = True

class LoanUpdate(BaseModel):
    actual_return_date: Optional[datetime]
    status: Optional[LoanStatus]

class LoanStatistics(BaseModel):
    total_loans: int
    active_loans: int
    overdue_loans: int