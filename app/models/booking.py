from sqlalchemy import Column, Integer, String, ForeignKey, Date, DATETIME, TIMESTAMP, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base
from restaurants_booking_app.app.models.table import Table
from restaurants_booking_app.app.models.user import User
from restaurants_booking_app.app.models.booking_status import Booking_Status


class Booking(Base):
    __tablename__ = "Booking"
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("User.user_id"))
    table_id = Column(Integer, ForeignKey("Table.table_id"))
    booking_date = Column(Date)
    booking_start_hours = Column(Integer)
    booking_end_hours = Column(Integer)
    booking_start_minutes = Column(Integer)
    booking_end_minutes = Column(Integer)
    booking_status_id = Column(Integer, ForeignKey("Booking_Status.booking_status_id"))
    booking_created_date = Column(Date)

    user = relationship("User")
    table = relationship("Table")
    status = relationship("Booking_Status")