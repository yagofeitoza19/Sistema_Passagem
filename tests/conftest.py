import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User
from app.auth import get_password_hash

# --- Configuração do Banco de Dados de Teste ---
# Usaremos um banco de dados SQLite em memória para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas no banco de dados de teste
Base.metadata.create_all(bind=engine)

# --- Sobrescrever a Dependência get_db ---
# Esta função será usada no lugar da `get_db` original durante os testes
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Aplicar a sobrescrita na aplicação FastAPI
app.dependency_overrides[get_db] = override_get_db

# --- Fixture do Cliente de Teste ---
# Cria um cliente para fazer requisições à API em cada teste
@pytest.fixture(scope="function")
def client():
    # Limpa e recria as tabelas antes de cada teste para garantir isolamento
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

# --- Fixture para Criar um Usuário de Teste ---
@pytest.fixture(scope="function")
def test_user():
    db = TestingSessionLocal()
    user = User(
        name="Test User",
        email="test@example.com",
        cpf="12345678900",
        password_hash=get_password_hash("testpassword"),
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"email": "test@example.com", "password": "testpassword"}