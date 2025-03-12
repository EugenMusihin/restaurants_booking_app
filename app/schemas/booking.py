from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime, timezone

class BookingCreate(BaseModel):
    user_id: int
    table_id: int
    booking_date: date
    booking_start_hours: int
    booking_end_hours: int
    booking_start_minutes: int
    booking_end_minutes: int
    booking_status_id: int
    booking_created_date: date

class BookingResponse(BaseModel):
    booking_id: int
    user_id: int
    table_id: int
    booking_date: date
    booking_start_hours: int
    booking_end_hours: int
    booking_start_minutes: int
    booking_end_minutes: int
    booking_status_id: int
    booking_created_date: date

    class Config:
        from_attributes = True