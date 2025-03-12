from pydantic import BaseModel
from datetime import date

class RestaurantCreate(BaseModel): 
    restaurant_name: str  
    restaurant_address: str  
    restaurant_phone: str  
    restaurant_created_date: date

class RestaurantResponse(BaseModel): 
    restaurant_id: int
    restaurant_name: str  
    restaurant_address: str 
    restaurant_phone: str  
    restaurant_created_date: date 
    class Config:
        from_attributes = True
