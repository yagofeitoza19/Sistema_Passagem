import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Settings(BaseModel):
    # Lendo as variáveis de ambiente para a conexão com o banco de dados
    DB_USER: str = os.getenv("POSTGRES_USER")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    DB_NAME: str = os.getenv("POSTGRES_DB")
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave-secreta-padrao")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Configurações de E-mail (RF14) ---
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"

# Instanciando a classe Settings
settings = Settings()