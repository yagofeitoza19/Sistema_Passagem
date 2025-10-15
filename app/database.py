from sqlalchemy import create_engine
# CORREÇÃO: Importar declarative_base do local correto
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# Configuração do banco de dados
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CORREÇÃO: Usar a função importada
Base = declarative_base()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()