from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from app.database.models import Booking
from app.schemas.booking import BookingCreate


def select_bookings(session: Session):
    query = select(Booking)
    result = session.execute(query)
    return result.all()


def create_booking(session: Session, booking_data: BookingCreate):

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

    return new_booking