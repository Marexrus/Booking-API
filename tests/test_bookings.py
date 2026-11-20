import pytest
from datetime import date, time, timedelta
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from app.routers.booking import add_booking, get_bookings
from app.schemas.booking import BookingCreate


@pytest.fixture
def session():
    return MagicMock()


@pytest.fixture
def booking_data():
    return BookingCreate(
        booking_date=date.today() + timedelta(days=1),
        booking_time=time(14, 0)
    )


# ---------- ADD BOOKING ----------

def test_add_booking(session, booking_data):
    with patch("app.routers.booking.create_booking", return_value=booking_data):
        result = add_booking(booking_data, session)

    assert result == booking_data


def test_add_booking_past_date(session, booking_data):
    booking_data.booking_date = date.today() - timedelta(days=1)

    with pytest.raises(HTTPException) as exc:
        add_booking(booking_data, session)

    assert exc.value.status_code == 422
    assert exc.value.detail == "Invalid date"


def test_add_booking_after_30_days(session, booking_data):
    booking_data.booking_date = date.today() + timedelta(days=30)

    with pytest.raises(HTTPException) as exc:
        add_booking(booking_data, session)

    assert exc.value.status_code == 422
    assert exc.value.detail == "Invalid date"


@pytest.mark.parametrize(
    "booking_time",
    [
        time(11, 0),
        time(14, 30),
        time(23, 0)
    ]
)
def test_add_booking_invalid_time(session, booking_data, booking_time):
    booking_data.booking_time = booking_time

    with pytest.raises(HTTPException) as exc:
        add_booking(booking_data, session)

    assert exc.value.status_code == 422
    assert exc.value.detail == "Invalid time"


def test_add_booking_duplicate(session, booking_data):
    with patch("app.routers.booking.create_booking", return_value=None):
        with pytest.raises(HTTPException) as exc:
            add_booking(booking_data, session)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Slot is already booked"


@pytest.mark.parametrize(
    "booking_time",
    [
        time(12, 0),
        time(14, 0),
        time(22, 0)
    ]
)
def test_add_booking_valid_time(session, booking_data, booking_time):
    booking_data.booking_time = booking_time

    with patch("app.routers.booking.create_booking", return_value=booking_data):
        result = add_booking(booking_data, session)

    assert result == booking_data


# ---------- GET BOOKINGS ----------

def test_get_bookings(session):
    expected = []

    with patch("app.routers.booking.select_bookings", return_value=expected):
        result = get_bookings(session=session)

    assert result == expected


def test_get_bookings_by_date(session):
    booking_date = date.today().isoformat()
    expected = []

    with patch("app.routers.booking.select_bookings", return_value=expected) as mock_select:
        result = get_bookings(booking_date=booking_date, session=session)

    assert result == expected
    mock_select.assert_called_once_with(session, date.fromisoformat(booking_date))