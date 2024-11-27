from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Campos de perfil e status
    is_active = Column(Boolean, default=True)
    is_librarian = Column(Boolean, default=False)
    
    # Campos de rastreamento
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relacionamentos
    loans = relationship("Loan", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    def hash_password(self, password):
        return pwd_context.hash(password)

    @property
    def active_loans(self):
        # Retorna apenas empréstimos ativos
        return [loan for loan in self.loans if loan.status == 'active']