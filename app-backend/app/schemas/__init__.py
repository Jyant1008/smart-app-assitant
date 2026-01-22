# schemas/__init__.py

# Makes 'schemas' a Python package
# Optional: import all schemas for easier access
from .user import UserCreate, UserRead, UserLogin
from .order import OrderCreate, OrderRead
from .payment import PaymentCreate, PaymentRead
