from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.admin import Admin
from restaurants_booking_app.app.schemas.admin import AdminCreate, AdminResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/post")
async def add_specific_userDiscounts(new_admin: AdminCreate, session: AsyncSession = Depends(get_db)):
    stmt = insert(Admin).values(**new_admin.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.delete("/{admin_id}")
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted"}
