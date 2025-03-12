from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base


class User_Role(Base):
    __tablename__ = "User_Role"
    user_role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_role_name = Column(String(100), unique=True, nullable=False)

    user = relationship("User", back_populates="user_role")
