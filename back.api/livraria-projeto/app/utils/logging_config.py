import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Configuração do logger raiz
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Log para console
            logging.StreamHandler(sys.stdout),
            # Log para arquivo com rotação
            RotatingFileHandler(
                'app.log', 
                maxBytes=10*1024*1024,  # 10 MB
                backupCount=5
            )
        ]
    )

def get_logger(name: str):
    """
    Retorna um logger para o módulo específico
    
    :param name: Nome do módulo/classe
    :return: Logger configurado
    """
    return logging.getLogger(name)