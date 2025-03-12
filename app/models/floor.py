from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base
from restaurants_booking_app.app.models.restraunt import Restaurant

class Floor(Base):
    __tablename__ = "Floor"
    floor_id = Column(Integer, primary_key=True, index=True)
    floor_name = Column(String(100), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("Restaurant.restaurant_id"))
    floor_created_date = Column(Date)

    restaurant = relationship("Restaurant")