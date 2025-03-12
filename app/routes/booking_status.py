from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.booking_status import Booking_Status
from restaurants_booking_app.app.schemas.bookin_status import BookingStatusCreate, BookingStatusResponse

router = APIRouter(
    prefix="/booking_status",
    tags=["Booking Status"]
)

@router.get("/", response_model=list[BookingStatusResponse])
async def get_booking_statuses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Booking_Status))
    return result.scalars().all()

@router.post("/post")
async def add_specific_userDiscounts(new_booking_status: BookingStatusCreate, session: AsyncSession = Depends(get_db)):
    stmt = insert(Booking_Status).values(**new_booking_status.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

