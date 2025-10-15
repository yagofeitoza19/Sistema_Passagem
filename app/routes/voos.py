from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db
from app.models import Flight
from app.schemas import Flight as FlightSchema
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import date, timedelta

router = APIRouter()

@router.get("/flights", response_model=List[FlightSchema], tags=["Flights"])
def get_flights(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    departure_date: Optional[date] = None,
    return_date: Optional[date] = None, # RF05
    passengers: Optional[int] = Query(1, ge=1), # RF05
    flight_class: Optional[str] = Query("Econômica", enum=["Econômica", "Executiva"]), # RF05
    sort_by: Optional[str] = Query(None, enum=["price", "duration", "departure_time"]), # RF07
    db: Session = Depends(get_db)
):
    query = db.query(Flight)

    # Filtros
    if origin:
        query = query.filter(Flight.origin.ilike(f"%{origin}%"))
    if destination:
        query = query.filter(Flight.destination.ilike(f"%{destination}%"))
    if departure_date:
        query = query.filter(Flight.departure_time >= departure_date)
    if passengers:
        query = query.filter(Flight.available_seats >= passengers)
    if flight_class:
        query = query.filter(Flight.flight_class == flight_class)
    
    # Ordenação (RF07)
    if sort_by:
        if sort_by == "price":
            query = query.order_by(Flight.price)
        elif sort_by == "duration":
            query = query.order_by(Flight.arrival_time - Flight.departure_time)
        elif sort_by == "departure_time":
            query = query.order_by(Flight.departure_time)
            
    return query.all()

@router.get("/flights/{flight_id}", response_model=FlightSchema, tags=["Flights"])
def get_flight_details(flight_id: int, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight