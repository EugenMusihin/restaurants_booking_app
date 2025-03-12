from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base
from restaurants_booking_app.app.models.user_role import User_Role
from datetime import date
from sqlalchemy.sql import func

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    user_phone = Column(String(12), unique=True)
    user_hash_password = Column(String(255), nullable=False)  # Храним хэшированный пароль
    user_role_id = Column(Integer, ForeignKey("User_Role.user_role_id"))
    user_created_date = Column(Date, default=func.current_date())  # Устанавливаем текущую дату

    user_role = relationship("User_Role")
    admin = relationship("Admin", back_populates = "user")

    def set_password(self, password: str):
        self.user_hash_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.user_hash_password)