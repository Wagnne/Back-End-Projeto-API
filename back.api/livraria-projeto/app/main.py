from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.controllers import user_controller  # Importe outros controllers conforme adicionar
from app.exceptions.custom_exceptions import (
    UserAlreadyExistsError, 
    UserNotFoundError
)
from app.utils.logging_config import setup_logging

# Configurar logging
logger = logging.getLogger(__name__)
setup_logging()

# Criar aplicação FastAPI
app = FastAPI(
    title="Library Management System",
    description="Sistema de Gerenciamento de Biblioteca",
    version="0.1.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos os origins em desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir roteadores dos controllers
app.include_router(user_controller.router)
# Incluir outros roteadores aqui

# Tratamento global de exceções
@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsError):
    logger.error(f"Erro de usuário existente: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )

@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    logger.error(f"Usuário não encontrado: {str(exc)}")
    return JSONResponse(
        status_code=404,
        content={"message": str(exc)}
    )

# Endpoint de saúde (health check)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Hook de inicialização da aplicação
@app.on_event("startup")
async def startup_event():
    logger.info("Aplicação iniciando...")

# Hook de desligamento da aplicação
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Aplicação desligando...")

# Permitir rodar o servidor diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)