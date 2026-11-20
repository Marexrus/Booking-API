from pydantic import BaseModel, field_serializer, Field
from datetime import date, time

class BookingCreate(BaseModel):
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=10)

    @field_serializer("booking_time")
    def serialize_booking_time(self, value: time):
        return value.strftime("%H:%M")

class BookingOut(BaseModel):
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int

    @field_serializer("booking_time")
    def serialize_booking_time(self, value: time):
        return value.strftime("%H:%M")