from pydantic import BaseModel, EmailStr, constr
from datetime import datetime, date
from typing import List, Optional

# --- Pagamento (RF11) ---
class PaymentDetails(BaseModel):
    card_name: str
    card_number: constr(min_length=16, max_length=16)
    expiry_month: int
    expiry_year: int
    cvv: constr(min_length=3, max_length=4)

# --- Passageiros ---
class PassengerBase(BaseModel):
    full_name: str
    document: str
    birth_date: date

class PassengerCreate(PassengerBase):
    pass

class Passenger(PassengerBase):
    id: int
    class Config:
        orm_mode = True

# --- Serviços Adicionais ---
class AdditionalServiceBase(BaseModel):
    name: str
    price: float

class AdditionalServiceCreate(AdditionalServiceBase):
    pass

class AdditionalService(AdditionalServiceBase):
    id: int
    class Config:
        orm_mode = True

# --- Reserva (Atualizado) ---
class ReservationBase(BaseModel):
    flight_id: int

class ReservationCreate(ReservationBase):
    passengers: List[PassengerCreate]
    additional_services: Optional[List[AdditionalServiceCreate]] = []

class Reservation(ReservationBase):
    id: int
    user_id: int
    status: str
    total_price: float
    payment_status: str
    passengers: List[Passenger] = []
    additional_services: List[AdditionalService] = [] # Adicionado para RF24
    
    class Config:
        orm_mode = True

# --- Voo ---
class FlightBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    airline: str
    available_seats: int
    price: float
    stops: int
    flight_class: str

class FlightCreate(FlightBase):
    pass

class Flight(FlightBase):
    id: int
    class Config:
        orm_mode = True

# --- Usuário ---
class UserBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str

class UserCreate(UserBase):
    password: constr(min_length=1, max_length=72)

class User(UserBase):
    id: int
    is_admin: bool
    class Config:
        orm_mode = True

# --- Auth ---
class UserLogin(BaseModel):
    email: str
    password: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str