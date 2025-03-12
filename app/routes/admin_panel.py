from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.booking import Booking
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.schemas.booking import BookingResponse, BookingResponse
from restaurants_booking_app.app.routes.auth import get_current_user
from typing import List

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

    result = await session.execute(select(Booking).options(joinedload(Booking.table)))
    bookings = result.scalars().all()
    return [BookingResponse.model_validate(booking) for booking in bookings]

@router.put("/update-status/{booking_id}")
async def update_booking_status(
    booking_id: int,
    update_data: BookingResponse,
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
