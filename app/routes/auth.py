from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.auth import create_access_token, verify_password, get_password_hash
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, PasswordResetRequest, PasswordReset
from sqlalchemy.orm import Session
from app.utils import send_email # RF14
import random
import string

router = APIRouter(tags=["Authentication"])
password_reset_tokens = {}

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        cpf=user.cpf,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"msg": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user and verify_password(user.password, db_user.password_hash):
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/request-password-reset")
async def request_password_reset(
    request: PasswordResetRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        password_reset_tokens[token] = user.email
        
        email_body = f"<h1>Redefinição de Senha</h1><p>Olá {user.name},</p><p>Use o seguinte token para redefinir a sua senha: <strong>{token}</strong></p>"
        background_tasks.add_task(send_email, "Redefinição de Senha", user.email, email_body)

    return {"msg": "Se existir uma conta com este e-mail, um link para redefinir a senha foi enviado."}

@router.post("/reset-password")
def reset_password(request: PasswordReset, db: Session = Depends(get_db)):
    email = password_reset_tokens.get(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
        
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.password_hash = get_password_hash(request.new_password)
    db.commit()
    
    del password_reset_tokens[request.token]
    
    return {"msg": "Password has been reset successfully."}