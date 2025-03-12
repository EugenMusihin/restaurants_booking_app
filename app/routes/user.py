from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.schemas.user import UserCreate, UserResponse
from restaurants_booking_app.app.routes.auth import get_current_user  # Функция для извлечения пользователя из токена

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
