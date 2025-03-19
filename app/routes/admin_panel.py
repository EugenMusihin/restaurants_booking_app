from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.booking import Booking
from restaurants_booking_app.app.models.table import Table
from restaurants_booking_app.app.models.floor import Floor
from restaurants_booking_app.app.models.restraunt import Restaurant
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.schemas.booking import BookingResponse
from restaurants_booking_app.app.routes.auth import get_current_user
from typing import List
from restaurants_booking_app.app.schemas.booking import BookingStatusUpdate

router = APIRouter(
    prefix="/admin/booking",
    tags=["Admin Booking"]
)

@router.get("/list", response_model=List[BookingResponse])
async def get_all_bookings(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_role_id != 2:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    result = await session.execute(
        select(Booking)
        .options(
            joinedload(Booking.table).joinedload(Table.floor).joinedload(Floor.restaurant)
        )
    )
    bookings = result.scalars().all()

    return [
        BookingResponse(
            booking_id=booking.booking_id,
            booking_date=booking.booking_date,
            booking_start_hours=booking.booking_start_hours,
            booking_end_hours=booking.booking_end_hours,
            booking_start_minutes=booking.booking_start_minutes,
            booking_end_minutes=booking.booking_end_minutes,
            booking_created_date=booking.booking_created_date,
            table_name=booking.table.table_number if booking.table else "Неизвестно",
            restaurant_name=booking.table.floor.restaurant.restaurant_name
            if booking.table and booking.table.floor and booking.table.floor.restaurant
            else "Неизвестно",
            user_id=booking.user_id,
            booking_status_id=booking.booking_status_id
        )
        for booking in bookings
    ]

@router.put("/update-status/{booking_id}")
async def update_booking_status(
    booking_id: int,
    update_data: BookingStatusUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_role_id != 2:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    result = await session.execute(select(Booking).where(Booking.booking_id == booking_id))
    booking = result.scalars().first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    booking.booking_status_id = update_data.booking_status_id
    await session.commit()
    return {"message": "Статус бронирования обновлен"}

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

