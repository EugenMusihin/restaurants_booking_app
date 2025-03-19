from pydantic import BaseModel
from datetime import date
from typing import Optional

class RestaurantCreate(BaseModel): 
    restaurant_name: str  
    restaurant_address: str  
    restaurant_phone: str  
    restaurant_created_date: date
    restaurant_open_hours: str
    restaurant_open_minutes: str
    restaurant_close_hours: str
    restaurant_close_minutes: str
    latitude: Optional[float] = None 
    longitude: Optional[float] = None 

class RestaurantResponse(BaseModel): 
    restaurant_id: int
    restaurant_name: str  
    restaurant_address: str 
    restaurant_phone: str  
    restaurant_created_date: date 
    restaurant_open_hours: str
    restaurant_open_minutes: str
    restaurant_close_hours: str
    restaurant_close_minutes: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True
