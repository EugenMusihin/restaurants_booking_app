from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.models.restraunt import Restaurant


class Admin(Base):
    __tablename__ = "Admin"

    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("Restaurant.restaurant_id"), nullable=False)
    admin_created_date = Column(Date)

    user = relationship("User", back_populates="admin")
    restaurant = relationship("Restaurant", back_populates="admin")
