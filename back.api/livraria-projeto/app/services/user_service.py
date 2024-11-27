from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.exceptions.custom_exceptions import UserAlreadyExistsError, UserNotFoundError

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, user: UserCreate):
        existing_user_email = self.user_repository.get_by_email(user.email)
        existing_user_username = self.user_repository.get_by_username(user.username)

        if existing_user_email:
            raise UserAlreadyExistsError("Email já cadastrado")
        
        if existing_user_username:
            raise UserAlreadyExistsError("Nome de usuário já existe")

        return self.user_repository.create(user)

    def update_user(self, user_id: int, user_update: UserUpdate):
        existing_user = self.user_repository.get_by_username(user_update.username)
        if existing_user and existing_user.id != user_id:
            raise UserAlreadyExistsError("Nome de usuário já existe")

        updated_user = self.user_repository.update(user_id, user_update)
        if not updated_user:
            raise UserNotFoundError("Usuário não encontrado")
        
        return updated_user