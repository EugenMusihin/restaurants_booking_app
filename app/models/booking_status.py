from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base

class Booking_Status(Base):
    __tablename__ = "Booking_Status"
    booking_status_id = Column(Integer, primary_key=True, index=True)
    booking_status_name = Column(String(100), unique=True, nullable=False)