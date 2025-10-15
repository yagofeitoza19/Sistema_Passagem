from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import json
from ..database import get_db
from ..models import Usuario, Administrador
from ..schemas import UsuarioCreate, UsuarioResponse, LoginRequest, Token
from ..auth import obter_hash_senha, verificar_senha, criar_access_token

router = APIRouter(prefix="/auth", tags=["autenticacao"])

@router.post("/registro", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se email já existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Verificar se CPF já existe
    db_usuario = db.query(Usuario).filter(Usuario.cpf == usuario.cpf).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    # Criar novo usuário
    hashed_password = obter_hash_senha(usuario.senha)
    db_usuario = Usuario(
        nome_completo=usuario.nome_completo,
        cpf=usuario.cpf,
        email=usuario.email,
        senha_hash=hashed_password
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return db_usuario

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuário por email
    usuario = db.query(Usuario).filter(Usuario.email == login_data.email).first()
    if not usuario or not verificar_senha(login_data.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Criar token de acesso
    access_token = criar_access_token(
        data={"sub": str(usuario.id), "is_admin": usuario.is_admin}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": usuario
    }

@router.post("/admin/login", response_model=dict)
def admin_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar administrador por email
    admin = db.query(Administrador).filter(Administrador.email == login_data.email).first()
    if not admin or not verificar_senha(login_data.senha, admin.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de administrador inválidas",
        )
    
    # Criar token de acesso para admin
    access_token = criar_access_token(
        data={"sub": str(admin.id), "is_admin": True}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin_id": admin.id,
        "nome": admin.nome
    }