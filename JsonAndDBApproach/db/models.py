from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)


# -----------------------------
# Base Class
# -----------------------------

class Base(DeclarativeBase):
    pass


# -----------------------------
# User Model
# -----------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


# -----------------------------
# Flight Model
# -----------------------------

class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(20), unique=True)

    origin: Mapped[str] = mapped_column(String(50))
    destination: Mapped[str] = mapped_column(String(50))

    departure_time: Mapped[datetime]
    arrival_time: Mapped[datetime]

    price: Mapped[float] = mapped_column(Float)

    # Relationships
    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="flight"
    )


# -----------------------------
# Booking Model
# -----------------------------

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)

    pnr: Mapped[str] = mapped_column(String(20), unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    flight_id: Mapped[int] = mapped_column(
        ForeignKey("flights.id")
    )

    booking_time: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="confirmed"
    )

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="bookings"
    )

    flight: Mapped["Flight"] = relationship(
        back_populates="bookings"
    )

    passengers: Mapped[list["Passenger"]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan"
    )


# -----------------------------
# Passenger Model
# -----------------------------

class Passenger(Base):
    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(primary_key=True)

    booking_id: Mapped[int] = mapped_column(
        ForeignKey("bookings.id")
    )

    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)

    # Relationship
    booking: Mapped["Booking"] = relationship(
        back_populates="passengers"
    )
