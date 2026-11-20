from pydantic import BaseModel, field_serializer, Field, ConfigDict
from typing import Literal
from datetime import date, time

class BookingCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    phone: str = Field(pattern=r'^\+7\d{10}$')
    booking_date: date
    booking_time: time
    guests: int = Field(ge=1, le=10)

class BookingOut(BaseModel):
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: Literal['active', 'cancelled']

    model_config = ConfigDict(from_attributes=True)