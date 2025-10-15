from app.database import engine
from app.models import Base

# Inicializando o banco de dados
Base.metadata.create_all(bind=engine)
