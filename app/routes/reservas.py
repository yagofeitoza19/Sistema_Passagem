from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.database import get_db
from app.models import Flight, Reservation, User, Passenger, AdditionalService
from app.schemas import ReservationCreate, Reservation as ReservationSchema, PaymentDetails
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.utils import send_email
from typing import List

router = APIRouter(tags=["Reservations"])

@router.post("/reserve", status_code=201, response_model=ReservationSchema)
def reserve(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # --- INÍCIO DO CÓDIGO DE DEBUG ---
    all_flights_in_db = db.query(Flight).all()
    print("--- DEBUG NA ROTA /reserve ---")
    if not all_flights_in_db:
        print("A base de dados não retornou nenhum voo neste momento.")
    else:
        print("Voos encontrados na base de dados:")
        for f in all_flights_in_db:
            print(f"  -> Voo ID: {f.id}, De: {f.origin} Para: {f.destination}")
    print("---------------------------------")
    # --- FIM DO CÓDIGO DE DEBUG ---

    flight = db.query(Flight).filter(Flight.id == reservation_data.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    if flight.available_seats < len(reservation_data.passengers):
        raise HTTPException(status_code=400, detail="No available seats for this number of passengers")

    total_price = flight.price * len(reservation_data.passengers)
    for service in reservation_data.additional_services:
        total_price += service.price

    new_reservation = Reservation(
        flight_id=reservation_data.flight_id,
        user_id=current_user.id,
        status="Pendente",
        total_price=total_price,
        payment_status="Pendente"
    )
    db.add(new_reservation)
    db.flush()
    
    for p in reservation_data.passengers:
        db.add(Passenger(**p.dict(), reservation_id=new_reservation.id))
    for s in reservation_data.additional_services:
        db.add(AdditionalService(**s.dict(), reservation_id=new_reservation.id))

    db.commit()
    db.refresh(new_reservation)
    return new_reservation

@router.post("/reservations/{reservation_id}/pay", status_code=200)
async def pay_for_reservation(
    reservation_id: int,
    payment_details: PaymentDetails,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    if reservation.payment_status == "Aprovado":
        raise HTTPException(status_code=400, detail="Reservation already paid")

    if not payment_details.card_number.endswith("1234"):
        reservation.payment_status = "Recusado"
        db.commit()
        raise HTTPException(status_code=400, detail="Payment declined")

    reservation.payment_status = "Aprovado"
    reservation.status = "Confirmada"
    db.commit()

    email_body = f"<h1>Compra Confirmada!</h1><p>Olá {current_user.name},</p><p>A sua reserva com o código <strong>#{reservation.id}</strong> foi confirmada com sucesso.</p>"
    background_tasks.add_task(send_email, "Confirmação de Compra", current_user.email, email_body)

    return {"msg": "Payment successful and reservation confirmed", "reservation_id": reservation.id}

@router.get("/reservations", response_model=List[ReservationSchema])
def get_reservations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()

@router.get("/reservations/{reservation_id}", response_model=ReservationSchema)
def get_reservation_details(reservation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id, Reservation.user_id == current_user.id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.delete("/reservations/{reservation_id}", status_code=200)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    flight = db.query(Flight).filter(Flight.id == reservation.flight_id).first()
    if flight and reservation.status == "Confirmada":
        flight.available_seats += len(reservation.passengers)
    
    db.delete(reservation)
    db.commit()

    return {"msg": "Reservation canceled successfully"}