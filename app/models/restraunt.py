from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base

class Restaurant(Base):
    __tablename__ = "Restaurant"
    restaurant_id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(120), nullable=False, unique=True)
    restaurant_address = Column(String(100), nullable=False)
    restaurant_phone = Column(String(12), unique=True)
    restaurant_created_date = Column(Date)

    admin = relationship("Admin", back_populates="restaurant")