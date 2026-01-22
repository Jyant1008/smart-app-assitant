#user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Used when creating a new user
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Used when returning user data
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        orm_mode = True  # allows reading from SQLAlchemy models

# Used for login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
