#order.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Used when creating an order
class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int
    total_price: float

# Used when returning order data
class OrderRead(BaseModel):
    id: int
    user_id: int
    product_name: str
    quantity: int
    total_price: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
