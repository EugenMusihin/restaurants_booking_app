from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from restaurants_booking_app.app.database import Base
from restaurants_booking_app.app.models.floor import Floor

class Table(Base):
    __tablename__ = "Table"
    table_id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, ForeignKey("Floor.floor_id"))
    table_number = Column(String(5), nullable=False)
    table_capacity = Column(Integer, nullable=False)
    table_created_date = Column(Date)

    floor = relationship("Floor")