from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.floor import Floor
from restaurants_booking_app.app.schemas.floor import FloorCreate, FloorResponse

router = APIRouter(
    prefix="/floor",
    tags=["Floor"]
)

@router.post("/post")
async def add_floor(new_floor: FloorCreate, session: AsyncSession = Depends(get_db)):
    stmt = insert(Floor).values(**new_floor.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.delete("/{floor_id}")
def delete_floor(floor_id: int, db: Session = Depends(get_db)):
    floor = db.query(Floor).filter(Floor.floor_id == floor_id).first()
    if not floor:
        return {"error": "Floor not found"}
    db.delete(floor)
    db.commit()
    return {"message": "Floor deleted"}

@router.get("/restaurant/{restaurant_id}")
async def get_floors_by_restaurant(restaurant_id: int, session: AsyncSession = Depends(get_db)):
    query = select(Floor).where(Floor.restaurant_id == restaurant_id)
    result = await session.execute(query)
    floors = result.scalars().all()
    return floors