from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

from datetime import date

from app.database.models import Booking
from app.schemas.booking import BookingCreate, BookingOut


def select_bookings(session: Session, booking_date: date | None = None) -> list[BookingOut] | None:
    if booking_date:
        query = select(Booking).where(Booking.booking_date == booking_date)
    else:
        query = select(Booking)

    result = session.scalars(query).all()

    return [BookingOut.model_validate(booking)for booking in result]


def select_booking_by_id(session: Session, booking_id: int) -> BookingOut | None:
    query = select(Booking).where(Booking.id == booking_id)
    booking = session.scalar(query)
    if booking is None:
        return None

    return BookingOut.model_validate(booking)


def delete_booking_by_id(session: Session, booking_id: int) -> BookingOut | None:
    stmt = update(Booking).where(Booking.id == booking_id).values(status='cancelled')
    result = session.execute(stmt)

    if result.rowcount == 0:
        session.rollback()
        return None
    session.commit()

    return select_booking_by_id(session, booking_id)


def create_booking(session: Session, booking_data: BookingCreate) -> BookingOut:

    # Проверяем, занят ли временной слот
    stmt = select(Booking).where(
        Booking.booking_date == booking_data.booking_date,
        Booking.booking_time == booking_data.booking_time,
        Booking.status == "active"
    )

    existing_booking = session.scalar(stmt)

    if existing_booking:
        return None

    # Создаём объект бронирования
    new_booking = Booking(
        name=booking_data.name,
        phone=booking_data.phone,
        booking_date=booking_data.booking_date,
        booking_time=booking_data.booking_time,
        guests=booking_data.guests
    )

    # Добавляем объект в сессию
    session.add(new_booking)

    # Сохраняем изменения в БД
    session.commit()

    # Обновляем объект данными из БД
    session.refresh(new_booking)

    return BookingOut.model_validate(new_booking)