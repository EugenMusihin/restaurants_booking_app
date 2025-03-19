from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.table import Table
from restaurants_booking_app.app.schemas.table import TableCreate, TableResponse
from typing import List

router = APIRouter(
    prefix="/table",
    tags=["Table"]
)
@router.post("/post")
async def add_specific_userDiscounts(new_table: TableCreate, session: AsyncSession = Depends(get_db)):
    stmt = insert(Table).values(**new_table.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.table_id == table_id).first()
    if not table:
        return {"error": "Table not found"}
    db.delete(table)
    db.commit()
    return {"message": "Table deleted"}

@router.get("/get", response_model=List[TableResponse])
async def get_tables(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Table))
    tables = result.scalars().all()
    if not tables:
        return []
    return [TableResponse.model_validate(table) for table in tables]

@router.get("/floor/{floor_id}", response_model=List[TableResponse])
async def get_tables_by_floor(floor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Table).where(Table.floor_id == floor_id))
    tables = result.scalars().all()
    
    if not tables:
        return []
    
    return [TableResponse.model_validate(table) for table in tables]

