from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200, 
        description="Título do livro"
    )
    author: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Autor do livro"
    )
    isbn: str = Field(
        ..., 
        min_length=10, 
        max_length=13, 
        description="ISBN do livro"
    )

class BookCreate(BookBase):
    publication_year: Optional[int] = Field(
        None, 
        ge=1000, 
        le=datetime.now().year, 
        description="Ano de publicação"
    )
    genre: Optional[str] = Field(
        None, 
        max_length=50
    )
    total_copies: int = Field(
        default=1, 
        ge=1, 
        description="Número total de cópias"
    )
    price: Optional[float] = Field(
        None, 
        ge=0, 
        description="Preço do livro"
    )

    @validator('isbn')
    def validate_isbn(cls, v):
        # Validação simples de ISBN
        # Pode ser substituída por uma validação mais robusta
        if not v.isdigit():
            raise ValueError('ISBN deve conter apenas números')
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=200
    )
    author: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=100
    )
    publication_year: Optional[int] = Field(
        None, 
        ge=1000, 
        le=datetime.now().year
    )
    genre: Optional[str] = Field(
        None, 
        max_length=50
    )
    total_copies: Optional[int] = Field(
        None, 
        ge=1
    )
    available_copies: Optional[int] = Field(
        None, 
        ge=0
    )
    is_active: Optional[bool] = None

class BookResponse(BookBase):
    id: int
    total_copies: int
    available_copies: int
    is_active: bool
    created_at: Optional[datetime]
    publication_year: Optional[int]
    genre: Optional[str]
    price: Optional[float]

    class Config:
        orm_mode = True
        from_attributes = True