from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from restaurants_booking_app.app.database import get_async_session as get_db
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.schemas.user import UserCreate
from sqlalchemy.future import select
from sqlalchemy import insert
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

class LoginRequest(BaseModel):
    email_or_phone: str
    password: str

SECRET_KEY = "SecretKey7525100" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register")
async def register_user(new_user: UserCreate, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User).where((User.user_email == new_user.user_email) | (User.user_phone == new_user.user_phone)))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email или телефон уже используются")

    hashed_password = pwd_context.hash(new_user.user_hash_password)
    
    user_data = new_user.model_dump()
    user_data["user_hash_password"] = hashed_password
    
    stmt = insert(User).values(**user_data)
    await session.execute(stmt)
    await session.commit()
    
    return {"message": "Пользователь зарегистрирован успешно"}

@router.post("/login")
async def login_user(login_data: LoginRequest, response: Response, session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(User).where((User.user_email == login_data.email_or_phone) | (User.user_phone == login_data.email_or_phone))
    )
    user = result.scalars().first()

    if not user or not pwd_context.verify(login_data.password, user.user_hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email/телефон или пароль")

    access_token = create_access_token(data={"sub": user.user_email})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=False,
        secure=True,
        samesite="None",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "Успешный вход", "redirect": True}


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отсутствует")

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка валидации токена")

    result = await session.execute(select(User).where(User.user_email == user_email))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=False,
        secure=True,
        samesite="None"
    ) 
    return {"message": "Вы вышли из системы"}

@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession= Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Не авторизован")

    return {
        "user_id": current_user.user_id,
        "user_name": current_user.user_name,
        "user_email": current_user.user_email,
        "user_phone": current_user.user_phone,
        "user_created_date": current_user.user_created_date,
        "user_role_id": current_user.user_role_id 
    }