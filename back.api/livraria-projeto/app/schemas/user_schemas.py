from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        description="Nome de usuário"
    )
    email: EmailStr = Field(
        ..., 
        description="Endereço de email"
    )
    full_name: Optional[str] = Field(
        None, 
        max_length=100, 
        description="Nome completo"
    )

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8, 
        description="Senha do usuário"
    )
    is_librarian: Optional[bool] = False

    @validator('password')
    def validate_password(cls, v):
        # Exemplo de validação de senha
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        
        # Verifica se a senha contém pelo menos:
        # - Uma letra maiúscula
        # - Uma letra minúscula
        # - Um número
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve conter pelo menos uma letra minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=50
    )
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(
        None, 
        max_length=100
    )
    password: Optional[str] = Field(
        None, 
        min_length=8
    )
    is_active: Optional[bool] = None

    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            # Reutiliza a validação de senha do UserCreate
            UserCreate.validate_password(v)
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_librarian: bool
    created_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str