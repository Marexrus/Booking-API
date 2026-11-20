from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import date, timedelta

from app.database.database import get_db
from app.services.booking_service import select_bookings, create_booking, select_booking_by_id, delete_booking_by_id
from app.schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get(path="/", response_model=list[BookingOut])
def get_bookings(booking_date: str | None = None, session=Depends(get_db)):
    if booking_date:
        booking_date = date.fromisoformat(booking_date)
    bookings = select_bookings(session, booking_date)
    print(bookings)
    return bookings


@router.get("/bookings/{booking_id}", response_model=BookingOut)
def get_booking_by_id(booking_id: int, session: Session = Depends(get_db)):
    booking = select_booking_by_id(session, booking_id)

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


@router.delete("/bookings/{booking_id}", response_model=BookingOut)
def delete_booking(booking_id: int, session: Session = Depends(get_db)):
    booking = delete_booking_by_id(session, booking_id)

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking


@router.post("/", response_model=BookingOut, status_code=201)
def add_booking(booking_data: BookingCreate, session: Session = Depends(get_db)):
    if booking_data.booking_date < date.today() or booking_data.booking_date >= date.today() + timedelta(days=30):
        raise HTTPException(status_code=422, detail='Invalid date')
    if booking_data.booking_time.minute != 00 or booking_data.booking_time.hour < 12 or booking_data.booking_time.hour > 22:
        raise HTTPException(status_code=422, detail='Invalid time')
    booking = create_booking(session, booking_data)

    if booking is None:
        raise HTTPException(
            status_code=409,
            detail="Slot is already booked"
        )

    return booking