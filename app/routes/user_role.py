from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.user_role import User_Role
from restaurants_booking_app.app.schemas.user_role import UserRoleCreate, UserRoleResponse

router = APIRouter(
    prefix="/user_role",
    tags=["User Role"]
)

@router.post("/post")
async def add_specific_userDiscounts(new_user: UserRoleCreate, session: AsyncSession = Depends(get_db)):
    stmt = insert(User_Role).values(**new_user.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.delete("/{role_id}")
def delete_user_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(User_Role).filter(User_Role.user_role_id == role_id).first()
    if not role:
        return {"error": "Role not found"}
    db.delete(role)
    db.commit()
    return {"message": "User role deleted"}
