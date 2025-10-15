from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from app.database import Base

# Modelo de voo
class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    airline = Column(String)
    available_seats = Column(Integer)
    price = Column(Float)
    stops = Column(Integer, default=0)
    flight_class = Column(String, default="Econômica")

# Modelo de usuário
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    cpf = Column(String, unique=True)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)

# Modelo de reserva
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    status = Column(String)
    total_price = Column(Float)
    payment_status = Column(String, default="Pendente")

    passengers = relationship("Passenger", back_populates="reservation", cascade="all, delete-orphan")
    additional_services = relationship("AdditionalService", back_populates="reservation", cascade="all, delete-orphan")

# Modelo de Passageiro
class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    full_name = Column(String)
    document = Column(String)
    birth_date = Column(Date)
    
    reservation = relationship("Reservation", back_populates="passengers")

# Modelo de Serviços Adicionais
class AdditionalService(Base):
    __tablename__ = "additional_services"
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"))
    name = Column(String)
    price = Column(Float)

    reservation = relationship("Reservation", back_populates="additional_services")