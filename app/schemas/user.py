from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
    user_hash_password: str
    user_role_id: int
    user_created_date: date

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    user_phone: str
    user_hash_password: str
    user_role_id: int
    user_created_date: date

    class Config:
        from_attributes = True
class UserLogin(BaseModel):
    user_email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    user_name: str
    user_email: EmailStr
    user_phone: str
