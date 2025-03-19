from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import select, insert
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.schemas.user import UserCreate, UserResponse, UserUpdate
from restaurants_booking_app.app.routes.auth import get_current_user
from restaurants_booking_app.app.models.booking import Booking
from restaurants_booking_app.app.models.table import Table
from restaurants_booking_app.app.schemas.booking import BookingResponse
from typing import List

from restaurants_booking_app.app.models.floor import Floor


router = APIRouter(
    prefix="/user",
    tags=["User"]
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/post")
async def add_user(new_user: UserCreate, session: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(new_user.user_hash_password) 
    user_data = new_user.model_dump()
    user_data["user_hash_password"] = hashed_password 
    stmt = insert(User).values(**user_data)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.delete("/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"error": "User not found"}
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@router.get("/get", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}
    return UserResponse.model_validate(user)

@router.get("/me", response_model=UserResponse)
async def get_current_user_data(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(current_user)

@router.get("/bookings", response_model=List[BookingResponse])
async def get_user_bookings(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(
        select(Booking)
        .options(
            joinedload(Booking.table).joinedload(Table.floor).joinedload(Floor.restaurant)
        )
        .where(Booking.user_id == current_user.user_id)
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

@router.put("/update")
async def update_user(
    updated_user: UserUpdate,
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_db)
):
    result = await session.execute(select(User).where(User.user_id == current_user.user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.user_name = updated_user.user_name
    user.user_email = updated_user.user_email
    user.user_phone = updated_user.user_phone

    await session.commit()
    return {"message": "User updated successfully"}
