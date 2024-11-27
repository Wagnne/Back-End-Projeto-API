from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.schemas.user_schemas import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> User:
        """
        Cria um novo usuário
        """
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=User.hash_password(user.password),
            is_librarian=user.is_librarian
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int) -> User:
        """
        Busca usuário pelo ID
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str):
        """
        Busca usuário pelo nome de usuário
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        """
        Busca usuário pelo email
        """
        return self.db.query(User).filter(User.email == email).first()

    def list_users(self, skip: int = 0, limit: int = 100):
        """
        Lista usuários com paginação
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, user_id: int, user_update: UserUpdate):
        """
        Atualiza dados do usuário
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            # Atualiza apenas os campos fornecidos
            update_data = user_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if key == 'password':
                    setattr(db_user, 'hashed_password', User.hash_password(value))
                else:
                    setattr(db_user, key, value)
            
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int):
        """
        Exclui usuário (ou marca como inativo)
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            # Exclusão lógica
            db_user.is_active = False
            self.db.commit()
        return db_user

    def update_last_login(self, user_id: int):
        """
        Atualiza o timestamp do último login
        """
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            db_user.last_login = func.now()
            self.db.commit()
        return db_user

    def count_users(self):
        """
        Conta o número total de usuários
        """
        return self.db.query(User).count()

    def authenticate_user(self, username: str, password: str):
        """
        Autentica usuário
        """
        user = self.get_by_username(username)
        if user and user.verify_password(password):
            return user
        return None