from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.booking import Booking
from restaurants_booking_app.app.schemas.booking import BookingCreate, BookingResponse
from restaurants_booking_app.app.models.table import Table
from typing import List

router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

@router.post("/post")
async def add_booking(new_booking: BookingCreate, session: AsyncSession = Depends(get_db)):
    query = select(Booking).where(
        and_(
            Booking.table_id == new_booking.table_id,
            Booking.booking_date == new_booking.booking_date,
            or_(
                and_(
                    Booking.booking_start_hours < new_booking.booking_end_hours,
                    Booking.booking_end_hours > new_booking.booking_start_hours
                ),
                and_(
                    Booking.booking_start_hours == new_booking.booking_start_hours,
                    Booking.booking_start_minutes < new_booking.booking_end_minutes
                )
            )
        )
    )
    existing_booking = await session.execute(query)
    if existing_booking.scalars().first():
        raise HTTPException(status_code=400, detail="Этот стол уже забронирован на указанное время")
    
    # Добавляем бронирование
    stmt = insert(Booking).values(**new_booking.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        return {"error": "Booking not found"}
    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted"}
@router.get("/", response_model=list[BookingResponse])
async def get_booking_statuses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking))
    return result.scalars().all()

@router.get("/available-tables/{floor_id}", response_model=List[int])
async def get_available_tables(floor_id: int, date: str, start_hour: int, start_minute: int, end_hour: int, end_minute: int, session: AsyncSession = Depends(get_db)):
    booked_query = select(Booking.table_id).where(
        and_(
            Booking.booking_date == date,
            or_(
                and_(
                    Booking.booking_start_hours < end_hour,
                    Booking.booking_end_hours > start_hour
                ),
                and_(
                    Booking.booking_start_hours == start_hour,
                    Booking.booking_start_minutes < end_minute
                )
            )
        )
    )
    booked_tables = (await session.execute(booked_query)).scalars().all()
    
    available_query = select(Table.table_id).where(
        and_(
            Table.floor_id == floor_id,
            Table.table_id.notin_(booked_tables)
        )
    )
    available_tables = (await session.execute(available_query)).scalars().all()
    return available_tables
