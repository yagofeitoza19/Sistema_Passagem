from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models import Flight, Reservation, User
# ATUALIZAÇÃO: FlightCreate foi movido para cá
from app.schemas import FlightCreate, User as UserSchema
from sqlalchemy.orm import Session
from app.auth import get_current_user
from typing import List

router = APIRouter()

# Dependência para verificar se o usuário é admin
def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized for this operation")
    return current_user

# ROTA MOVIDA DE voos.py PARA CÁ
@router.post("/add-flight", summary="Adicionar um novo voo")
def add_flight(flight: FlightCreate, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    db_flight = Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    return {"msg": "Flight added successfully"}

# Rota para editar voo (protegida)
@router.put("/edit-flight/{flight_id}", summary="Editar um voo existente")
def edit_flight(flight_id: int, flight: FlightCreate, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    db_flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    for key, value in flight.dict().items():
        setattr(db_flight, key, value)
    db.commit()
    return {"msg": "Flight updated successfully"}

# Rota para excluir voo (protegida)
@router.delete("/delete-flight/{flight_id}", summary="Excluir um voo")
def delete_flight(flight_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    reservations = db.query(Reservation).filter(Reservation.flight_id == flight_id).count()
    if reservations > 0:
        raise HTTPException(status_code=400, detail="Cannot delete flight with active reservations")
        
    db_flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not db_flight:
        raise HTTPException(status_code=404, detail="Flight not found")
        
    db.delete(db_flight)
    db.commit()
    return {"msg": "Flight deleted successfully"}

# Rota para listar todos os usuários (protegida)
@router.get("/users", response_model=List[UserSchema], summary="Listar todos os usuários")
def list_users(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    users = db.query(User).all()
    return users

# Rota para tornar um usuário administrador (protegida)
@router.put("/users/{user_id}/make-admin", summary="Tornar um usuário administrador")
def make_user_admin(user_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    user_to_promote = db.query(User).filter(User.id == user_id).first()
    if not user_to_promote:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_to_promote.is_admin = True
    db.commit()
    
    return {"msg": f"User '{user_to_promote.name}' is now an administrator."}