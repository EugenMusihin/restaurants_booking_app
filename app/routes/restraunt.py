from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.restraunt import Restaurant
from restaurants_booking_app.app.schemas.restraunt import RestaurantCreate, RestaurantResponse
from typing import List

router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)

@router.post("/post")
async def add_specific_restaurant(new_restaurant: RestaurantCreate, session: AsyncSession = Depends(get_db)):
    stmt = insert(Restaurant).values(**new_restaurant.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        return {"error": "Restaurant not found"}
    db.delete(restaurant)
    db.commit()
    return {"message": "Restaurant deleted"}

@router.get("/get", response_model=List[RestaurantResponse])
async def get_restraunts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Restaurant))
    tables = result.scalars().all()
    if not tables:
        return []
    return [RestaurantResponse.model_validate(table) for table in tables]