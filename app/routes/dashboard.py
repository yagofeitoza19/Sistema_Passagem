from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import get_db
from app.models import Reservation, User, Flight
from app.schemas import Reservation as ReservationSchema
from app.auth import get_current_user
from typing import List

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    total_reservas = db.query(Reservation).count()
    reservas_confirmadas = db.query(Reservation).filter(Reservation.status == "Confirmada").count()
    receita_total = db.query(func.sum(Reservation.total_price)).filter(Reservation.status == "Confirmada").scalar() or 0
    voos_ativos = db.query(Flight).filter(Flight.departure_time >= func.now()).count()
    
    return {
        "total_reservas": total_reservas,
        "reservas_confirmadas": reservas_confirmadas,
        "receita_total": receita_total,
        "voos_ativos": voos_ativos
    }

@router.get("/reservations", response_model=List[ReservationSchema])
def list_admin_reservations(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    return db.query(Reservation).all()

@router.get("/reservations/{reservation_id}", response_model=ReservationSchema)
def get_detailed_reservation_admin(
    reservation_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    reservation = db.query(Reservation).options(
        joinedload(Reservation.passengers),
        joinedload(Reservation.additional_services)
    ).filter(Reservation.id == reservation_id).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return reservation