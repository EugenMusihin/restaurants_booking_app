from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base

class Restaurant(Base):
    __tablename__ = "Restaurant"

    restaurant_id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(120), nullable=False, unique=True)
    restaurant_address = Column(String(100), nullable=False)
    restaurant_phone = Column(String(12), unique=True)
    restaurant_created_date = Column(Date)
    restaurant_open_hours = Column(String(2))
    restaurant_open_minutes = Column(String(2))
    restaurant_close_hours = Column(String(2))
    restaurant_close_minutes = Column(String(2))

    latitude = Column(Float, nullable=True)   # Добавили широту
    longitude = Column(Float, nullable=True)  # Добавили долготу

    admin = relationship("Admin", back_populates="restaurant")
