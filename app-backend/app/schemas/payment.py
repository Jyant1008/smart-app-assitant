#payment.py
from pydantic import BaseModel
from datetime import datetime

# Used when creating a payment
class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str = "online"

# Used when returning payment data
class PaymentRead(BaseModel):
    id: int
    order_id: int
    amount: float
    method: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
