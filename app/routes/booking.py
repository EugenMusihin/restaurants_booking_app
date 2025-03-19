from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.booking import Booking
from restaurants_booking_app.app.schemas.booking import BookingCreate, BookingResponse
from restaurants_booking_app.app.models.table import Table
from restaurants_booking_app.app.models.floor import Floor
from restaurants_booking_app.app.models.restraunt import Restaurant
from datetime import time
from typing import List

router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

@router.post("/post")
async def add_booking(new_booking: BookingCreate, session: AsyncSession = Depends(get_db)):
    restaurant_query = (
        select(Restaurant)
        .join(Floor, Floor.restaurant_id == Restaurant.restaurant_id)
        .join(Table, Table.floor_id == Floor.floor_id)
        .where(Table.table_id == new_booking.table_id)
    )    
    restaurant = (await session.execute(restaurant_query)).scalars().first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Ресторан не найден")
    open_time = time(int(restaurant.restaurant_open_hours), int(restaurant.restaurant_open_minutes))
    close_time = time(int(restaurant.restaurant_close_hours), int(restaurant.restaurant_close_minutes))
    booking_start = time(new_booking.booking_start_hours, new_booking.booking_start_minutes)
    booking_end = time(new_booking.booking_end_hours, new_booking.booking_end_minutes)
    if (
        new_booking.booking_start_hours not in range(24) or
        new_booking.booking_end_hours not in range(24) or
        new_booking.booking_start_minutes not in range(60) or
        new_booking.booking_end_minutes not in range(60)
    ):
        raise HTTPException(status_code=400, detail="Некорректное время бронирования")
    if booking_start < open_time or booking_end > close_time:
        raise HTTPException(status_code=400, detail="Бронирование возможно только в рабочее время ресторана")
    if booking_start >= booking_end:
        raise HTTPException(status_code=400, detail="Время окончания бронирования должно быть позже времени начала")
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
    stmt = insert(Booking).values(**new_booking.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/delete/{booking_id}")
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Booking).filter(Booking.booking_id == booking_id)
    result = await db.execute(query)
    booking = result.scalars().first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    
    await db.delete(booking)
    await db.commit()
    
    return {"message": "Бронирование удалено"}

@router.get("/", response_model=list[BookingResponse])
async def get_bookings(db: AsyncSession = Depends(get_db)):
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
