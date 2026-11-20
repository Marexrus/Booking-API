from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.booking_service import select_bookings, create_booking
from app.schemas.booking import BookingCreate, BookingOut

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get(path="/")
def get_bookings(date: str | None = None, session=Depends(get_db)):
    bookings = select_bookings(session)
    print(bookings)
    return bookings


@router.post("/", response_model=BookingOut, status_code=201)
def add_booking(booking_data: BookingCreate, session: Session = Depends(get_db)):
    booking = create_booking(session, booking_data)

    if booking is None:
        raise HTTPException(
            status_code=409,
            detail="Slot is already booked"
        )

    return booking