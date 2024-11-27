import pytest
from fastapi import HTTPException

from app.services.user_service import UserService
from app.schemas.user_schemas import UserCreate, UserUpdate

def test_create_user(test_db, sample_user):
    user_service = UserService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    assert created_user.name == sample_user['name']
    assert created_user.email == sample_user['email']

def test_create_duplicate_user(test_db, sample_user):
    user_service = UserService(test_db)
    
    # Cria primeiro usuário
    user_create = UserCreate(**sample_user)
    user_service.create_user(user_create)
    
    # Tenta criar usuário com mesmo email
    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(user_create)
    
    assert exc_info.value.status_code == 400
    assert "Email already registered" in str(exc_info.value.detail)

def test_authenticate_user(test_db, sample_user):
    user_service = UserService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    user_service.create_user(user_create)
    
    # Autentica usuário
    authenticated_user = user_service.authenticate_user(
        sample_user['email'], 
        sample_user['password']
    )
    
    assert authenticated_user is not None
    assert authenticated_user.email == sample_user['email']

def test_authenticate_invalid_user(test_db, sample_user):
    user_service = UserService(test_db)
    
    # Tenta autenticar usuário não existente
    authenticated_user = user_service.authenticate_user(
        sample_user['email'], 
        sample_user['password']
    )
    
    assert authenticated_user is None

def test_update_user(test_db, sample_user):
    user_service = UserService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    # Atualiza usuário
    update_data = UserUpdate(name="Updated Name")
    updated_user = user_service.update_user(created_user.id, update_data)
    
    assert updated_user.name == "Updated Name"

def test_delete_user(test_db, sample_user):
    user_service = UserService(test_db)
    
    # Cria usuário
    user_create = UserCreate(**sample_user)
    created_user = user_service.create_user(user_create)
    
    # Deleta usuário
    user_service.delete_user(created_user.id)
    
    # Verifica se usuário não pode ser encontrado
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_id(created_user.id)
    
    assert exc_info.value.status_code == 404