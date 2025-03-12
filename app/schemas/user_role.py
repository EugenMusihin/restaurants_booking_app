from pydantic import BaseModel, EmailStr
from datetime import date

class UserRoleCreate(BaseModel):
    user_role_name: str
    

class UserRoleResponse(BaseModel):
    user_role_id: int
    user_role_name: str
    
    class Config:
        from_attributes = True
